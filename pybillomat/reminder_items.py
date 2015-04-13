#!/usr/bin/env python
# coding: utf-8
"""
Reminder-Items

- English API-Description: http://www.billomat.com/en/api/reminders/items
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/mahnungen/positionen/
"""

import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _reminder_item_xml(
    reminder_id = None,
    article_id = None,
    unit = None,
    quantity = None,
    unit_price = None,
    title = None,
    description = None
):
    """
    Creates the XML to add or edit a reminder-item
    """

    integer_field_names = [
        "reminder_id",
        "article_id",
    ]
    float_fieldnames = [
        "quantity",
        "unit_price",
    ]
    string_fieldnames = [
        "unit",
        "title",
        "description",
    ]

    reminder_item_tag = ET.Element("reminder-item")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            reminder_item_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            reminder_item_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            reminder_item_tag.append(new_tag)

    xml = ET.tostring(reminder_item_tag)

    # Finished
    return xml


class ReminderItem(Item):

    base_path = u"/api/reminder-items"


    def __init__(self, conn, id = None, reminder_item_etree = None):
        """
        Reminder-Item

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.created = None  # datetime
        self.article_id = None
        self.reminder_id = None  # integer
        self.position = None  # integer
        self.unit = None
        self.quantity = None  # float
        self.unit_price = None  # float
        self.title = None
        self.description = None
        self.total = None  # float

        if reminder_item_etree is not None:
            self.load_from_etree(reminder_item_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        reminder_id = None,
        article_id = None,
        unit = None,
        quantity = None,
        unit_price = None,
        title = None,
        description = None
    ):
        """
        Creates a reminder-item

        :param conn: Connection-Object

        :param reminder_id: ID of the reminder
        :param article_id: ID of the article, sets additionally the values
            from the article on creation.
        :param unit: Unit
        :param quantity: Quantity
        :param unit_price: Price per unit
        :param title: Title
        :param description: Description
        """

        # XML
        xml = _reminder_item_xml(
            reminder_id = reminder_id,
            article_id = article_id,
            unit = unit,
            quantity = quantity,
            unit_price = unit_price,
            title = title,
            description = description,
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Reminder-Object
        reminder = cls(conn = conn)
        reminder.content_language = response.headers.get("content-language", None)
        reminder.load_from_xml(response.data)

        # Finished
        return reminder


    def edit(
        self,
        id = None,
        article_id = None,
        unit = None,
        quantity = None,
        unit_price = None,
        title = None,
        description = None
    ):
        """
        Edit a reminder-item

        :param id: ID of the reminder-item

        :param article_id: ID of the article, sets additionally the values
            from the article on creation.
        :param unit: Unit
        :param quantity: Quantity
        :param unit_price: Price per unit
        :param title: Title
        :param description: Description
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _reminder_item_xml(
            article_id = article_id,
            unit = unit,
            quantity = quantity,
            unit_price = unit_price,
            title = title,
            description = description
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


class ReminderItems(list):

    def __init__(self, conn):
        """
        ReminderItems-List

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
        reminder_id = None,

        order_by = None,
        fetch_all = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with ReminderItem-objects

        :param reminder_id: ID of the reminder (mandatory)

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        """

        # Check empty param
        if not reminder_id:
            raise errors.EmptyFilterError()

        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Url and system-parameters
        url = Url(path = "/api/reminder-items")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameter
        url.query["reminder_id"] = reminder_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        reminder_items_etree = ET.fromstring(response.data)

        self.per_page = int(reminder_items_etree.attrib.get("per_page", "100"))
        self.total = int(reminder_items_etree.attrib.get("total", "0"))
        self.page = int(reminder_items_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all items
        for reminder_item_etree in reminder_items_etree:
            self.append(
                ReminderItem(conn = self.conn, reminder_item_etree = reminder_item_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                reminder_id = reminder_id,

                order_by = order_by,
                fetch_all = fetch_all,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class ReminderItemsIterator(ItemsIterator):
    """
    Iterates over all found reminders
    """

    def __init__(self, conn, per_page = 30):
        """
        ReminderItemsIterator
        """

        self.conn = conn
        self.items = ReminderItems(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            reminder_id = None,
            order_by = None
        )


    def search(
        self,
        reminder_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.reminder_id = reminder_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            reminder_id = self.search_params.reminder_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


