#!/usr/bin/env python
# coding: utf-8
"""
Settings: Reminder-Texts

- English API-Description: http://www.billomat.com/en/api/settings/reminder-texts
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/einstellungen/mahnstufen
"""

import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _reminder_text_xml(
    sorting = None,
    name = None,
    subject = None,
    header = None,
    footer = None,
    charge_name = None,
    charge_description = None,
    charge_amount = None
):
    """
    Creates the XML to add or edit an email template
    """

    string_fieldnames = [
        "name",
        "subject",
        "header",
        "footer",
        "charge_name",
        "charge_description",
    ]
    integer_fieldnames = [
        "sorting",
    ]
    float_fieldnames = [
        "charge_amount",
    ]

    reminder_text_tag = ET.Element("email-template")

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            reminder_text_tag.append(new_tag)

    # Integer Fields
    for field_name in integer_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            reminder_text_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            reminder_text_tag.append(new_tag)

    # Finished
    xml = ET.tostring(reminder_text_tag)
    return xml


class ReminderText(Item):

    base_path = u"/api/reminder-texts"


    def __init__(self, conn, id = None, reminder_text_etree = None):
        """
        ReminderText

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # Integer
        self.sorting = None  # Integer
        self.name = None
        self.subject = None
        self.header = None
        self.footer = None
        self.charge_name = None
        self.charge_description = None
        self.charge_amount = None  # Float

        if reminder_text_etree is not None:
            self.load_from_etree(reminder_text_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        sorting = None,
        name = None,
        subject = None,
        header = None,
        footer = None,
        charge_name = None,
        charge_description = None,
        charge_amount = None
    ):
        """
        Creates an email template

        :param conn: Connection-Object
        :param sorting: The sorting of this reminder text;
            Without a sorting the reminder text it placed at the end of all
            reminder texts.
        :param name: A name for internal use only
        :param subject: A subject.
        :param header: Introductory text
        :param footer: xplanatory notes
        :param charge_name: Name of charge (if present)
        :param charge_description: Description of charge (if present)
        :param charge_amount: Ammount of charge (if present)
        """

        # XML
        xml = _reminder_text_xml(
            sorting = sorting,
            name = name,
            subject = subject,
            header = header,
            footer = footer,
            charge_name = charge_name,
            charge_description = charge_description,
            charge_amount = charge_amount
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create ReminderText-Object
        reminder_text = cls(conn = conn)
        reminder_text.content_language = response.headers.get("content-language", None)
        reminder_text.load_from_xml(response.data)

        # Finished
        return reminder_text


    def edit(
        self,
        id = None,

        sorting = None,
        name = None,
        subject = None,
        header = None,
        footer = None,
        charge_name = None,
        charge_description = None,
        charge_amount = None
    ):
        """
        Edit one email template

        :param sorting: The sorting of this reminder text;
            Without a sorting the reminder text it placed at the end of all
            reminder texts.
        :param name: A name for internal use only
        :param subject: A subject.
        :param header: Introductory text
        :param footer: xplanatory notes
        :param charge_name: Name of charge (if present)
        :param charge_description: Description of charge (if present)
        :param charge_amount: Ammount of charge (if present)
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _reminder_text_xml(
            sorting = sorting,
            name = name,
            subject = subject,
            header = header,
            footer = footer,
            charge_name = charge_name,
            charge_description = charge_description,
            charge_amount = charge_amount
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


class ReminderTexts(list):

    def __init__(self, conn):
        """
        ReminderTexts-List

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
        Fills the (internal) list with ReminderText-objects

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
        url = Url(path = "/api/reminder-texts")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        reminder_texts_etree = ET.fromstring(response.data)

        self.per_page = int(reminder_texts_etree.attrib.get("per_page", "0"))
        self.total = int(reminder_texts_etree.attrib.get("total", "0"))
        self.page = int(reminder_texts_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all email templates
        for reminder_text_etree in reminder_texts_etree:
            self.append(
                ReminderText(
                    conn = self.conn,
                    reminder_text_etree = reminder_text_etree
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


class ReminderTextsIterator(ItemsIterator):
    """
    Iterates over all found email templates
    """

    def __init__(self, conn, per_page = 30):
        """
        ReminderTextsIterator
        """

        self.conn = conn
        self.items = ReminderTexts(self.conn)
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


