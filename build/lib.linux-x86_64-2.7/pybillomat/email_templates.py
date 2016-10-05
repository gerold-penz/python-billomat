#!/usr/bin/env python
# coding: utf-8
"""
Email-Templates

- English API-Description: http://www.billomat.com/de/api/einstellungen/email-vorlagen
- Deutsche API-Beschreibung: http://www.billomat.com/en/api/settings/email-vorlagen
"""

import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _email_template_xml(
    name = None,
    type = None,
    subject = None,
    text = None,
    bcc = None,
    is_default = None
):
    """
    Creates the XML to add or edit an email template
    """

    string_fieldnames = [
        "name",
        "type",
        "subject",
        "text",
    ]
    boolean_fieldnames = [
        "bcc",
        "is_default"
    ]

    email_template_tag = ET.Element("email-template")

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            email_template_tag.append(new_tag)

    # Boolean Fields
    for field_name in boolean_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = "1" if value else "0"
            email_template_tag.append(new_tag)

    # Finished
    xml = ET.tostring(email_template_tag)
    return xml


class EmailTemplate(Item):

    base_path = u"/api/email-templates"


    def __init__(self, conn, id = None, email_template_etree = None):
        """
        EmailTemplate

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # Integer
        self.name = None
        self.type = None
        self.subject = None
        self.text = None
        self.bcc = None  # Boolean
        self.is_default = None  # Boolean

        if email_template_etree is not None:
            self.load_from_etree(email_template_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        name = None,
        type = None,
        subject = None,
        text = None,
        bcc = None,
        is_default = None
    ):
        """
        Creates an email template

        :param conn: Connection-Object
        :param name: Name of the template; mandatory
        :param type: Document type; mandatory
        :param subject: Subject
        :param text: Message text
        :param bcc: Specifies whether the sender should get a copy as BCC;
            boolean;
        :param is_default: Specifies whether this is the standard template;
            boolean;
        """

        # XML
        xml = _email_template_xml(
            name = name,
            type = type,
            subject = subject,
            text = text,
            bcc = bcc,
            is_default = is_default
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create EmailTemplate-Object
        email_template = cls(conn = conn)
        email_template.content_language = response.headers.get("content-language", None)
        email_template.load_from_xml(response.data)

        # Finished
        return email_template


    def edit(
        self,
        id = None,
        name = None,
        type = None,
        subject = None,
        text = None,
        bcc = None,
        is_default = None
    ):
        """
        Edit one email template

        :param name: Name of the template; mandatory
        :param type: Document type; mandatory
        :param subject: Subject
        :param text: Message text
        :param bcc: Specifies whether the sender should get a copy as BCC;
            boolean;
        :param is_default: Specifies whether this is the standard template;
            boolean;
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _email_template_xml(
            name = name,
            type = type,
            subject = subject,
            text = text,
            bcc = bcc,
            is_default = is_default
        )

        # Path
        path = "{base_path}/{id}".format(
            base_path = self.base_path,
            id = self.id
        )

        # Send PUT-request
        response = self.conn.put(path = path, body = xml)
        if response.status != 200:  # Edited
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))


class EmailTemplates(list):

    def __init__(self, conn):
        """
        EmailTemplates-List

        :param conn: Connection-Object
        """

        list.__init__(self)

        self.conn = conn
        self.per_page = None
        self.total = None
        self.page = None
        self.pages = None


    def search(
        self,
        # Search parameters
        order_by = None,

        fetch_all = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the (internal) list with EmailTemplate-objects

        If no search criteria given --> all email templates will returned (REALLY ALL!).

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.
        """
        
        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Url and system-parameters
        url = Url(path = "/api/email-templates")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        email_templates_etree = ET.fromstring(response.data)

        self.per_page = int(email_templates_etree.attrib.get("per_page", "0"))
        self.total = int(email_templates_etree.attrib.get("total", "0"))
        self.page = int(email_templates_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all email templates
        for email_template_etree in email_templates_etree:
            self.append(
                EmailTemplate(
                    conn = self.conn,
                    email_template_etree = email_template_etree
                )
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                order_by = order_by,
                fetch_all = fetch_all,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class EmailTemplatesIterator(ItemsIterator):
    """
    Iterates over all found email templates
    """

    def __init__(self, conn, per_page = 30):
        """
        EmailTemplatesIterator
        """

        self.conn = conn
        self.items = EmailTemplates(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            order_by = None,
        )


    def search(
        self,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            order_by = self.search_params.order_by,
            fetch_all = False,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


