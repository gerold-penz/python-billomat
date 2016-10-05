#!/usr/bin/env python
# coding: utf-8
"""
Recurring Email Receivers

- English API-Description: http://www.billomat.com/en/api/recurrings/receivers
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/abo-rechnungen/empfaenger
"""


import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _recurring_email_receiver_xml(
    recurring_id = None,
    type = None,
    address = None
):
    """
    Creates the XML to add or edit a recurring-email_receiver
    """

    integer_field_names = [
        "recurring_id",
    ]
    string_fieldnames = [
        "type",
        "address",
    ]

    recurring_email_receiver_tag = ET.Element("recurring-email-receiver")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            recurring_email_receiver_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            recurring_email_receiver_tag.append(new_tag)

    xml = ET.tostring(recurring_email_receiver_tag)

    # Finished
    return xml


class RecurringEmailReceiver(Item):

    base_path = u"/api/recurring-email-receivers"


    def __init__(self, conn, id = None, recurring_email_receiver_etree = None):
        """
        Recurring-Item

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.recurring_id = None  # integer
        self.type = None
        self.address = None

        if recurring_email_receiver_etree is not None:
            self.load_from_etree(recurring_email_receiver_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        recurring_id = None,
        type = None,
        address = None
    ):
        """
        Creates a recurring-email_receiver

        :param conn: Connection-Object

        :param recurring_id: ID of the recurring
        :param type: Receiver type (to, cc, bcc)
        :param address: Email address
        """

        # XML
        xml = _recurring_email_receiver_xml(
            recurring_id = recurring_id,
            type = type,
            address = address
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Recurring-Email-Receiver-Object
        recurring = cls(conn = conn)
        recurring.content_language = response.headers.get("content-language", None)
        recurring.load_from_xml(response.data)

        # Finished
        return recurring


    def edit(
        self,
        id = None,
        type = None,
        address = None
    ):
        """
        Edit a recurring-email_receiver

        :param id: ID of the recurring-email_receiver
        :param type: Receiver type (to, cc, bcc); mandatory
        :param address: Email address; mandatory; Empty address resets to the
            default address.
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _recurring_email_receiver_xml(
            type = type,
            address = address
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


class RecurringEmailReceivers(list):

    def __init__(self, conn):
        """
        RecurringEmailReceivers-List

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
        recurring_id = None,

        order_by = None,
        fetch_all = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with RecurringItem-objects

        :param recurring_id: ID of the recurring (mandatory)

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.
        """

        # Check empty param
        if not recurring_id:
            raise errors.EmptyFilterError()

        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Url and system-parameters
        url = Url(path = "/api/recurring-email-receivers")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameter
        url.query["recurring_id"] = recurring_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        recurring_email_receivers_etree = ET.fromstring(response.data)

        self.per_page = int(recurring_email_receivers_etree.attrib.get("per_page", "100"))
        self.total = int(recurring_email_receivers_etree.attrib.get("total", "0"))
        self.page = int(recurring_email_receivers_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all items
        for recurring_email_receiver_etree in recurring_email_receivers_etree:
            self.append(
                RecurringEmailReceiver(
                    conn = self.conn,
                    recurring_email_receiver_etree = recurring_email_receiver_etree
                )
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                recurring_id = recurring_id,

                order_by = order_by,
                fetch_all = fetch_all,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class RecurringEmailReceiversIterator(ItemsIterator):
    """
    Iterates over all found recurrings
    """

    def __init__(self, conn, per_page = 30):
        """
        RecurringItemsIterator
        """

        self.conn = conn
        self.items = RecurringEmailReceivers(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            recurring_id = None,
            order_by = None
        )


    def search(
        self,
        recurring_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.recurring_id = recurring_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            recurring_id = self.search_params.recurring_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


