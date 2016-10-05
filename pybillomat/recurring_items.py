#!/usr/bin/env python
# coding: utf-8
"""
Recurring-Items

- English API-Description: http://www.billomat.com/en/api/recurrings/items
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/abo-rechnungen/positionen
"""


import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _recurring_item_xml(
    recurring_id = None,
    article_id = None,
    unit = None,
    quantity = None,
    unit_price = None,
    tax_name = None,
    tax_rate = None,
    title = None,
    description = None,
    reduction = None
):
    """
    Creates the XML to add or edit a recurring-item
    """

    integer_fieldnames = [
        "recurring_id",
        "article_id",
    ]
    float_fieldnames = [
        "quantity",
        "unit_price",
        "tax_rate",
    ]
    string_fieldnames = [
        "unit",
        "tax_name",
        "title",
        "description",
        "reduction",
    ]

    recurring_item_tag = ET.Element("recurring-item")

    # Integer Fields
    for field_name in integer_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            recurring_item_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            recurring_item_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            recurring_item_tag.append(new_tag)

    xml = ET.tostring(recurring_item_tag)

    # Finished
    return xml


class RecurringItem(Item):

    base_path = u"/api/recurring-items"


    def __init__(self, conn, id = None, recurring_item_etree = None):
        """
        Recurring-Item

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.created = None  # datetime
        self.article_id = None
        self.recurring_id = None  # integer
        self.position = None  # integer
        self.unit = None
        self.quantity = None  # float
        self.unit_price = None  # float
        self.tax_name = None
        self.tax_rate = None  # float
        self.title = None
        self.description = None
        self.total_gross = None  # float
        self.total_net = None  # float
        self.reduction = None
        self.total_gross_unreduced = None  # float
        self.total_net_unreduced = None  # float

        if recurring_item_etree is not None:
            self.load_from_etree(recurring_item_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        recurring_id = None,
        article_id = None,
        unit = None,
        quantity = None,
        unit_price = None,
        tax_name = None,
        tax_rate = None,
        title = None,
        description = None,
        reduction = None
    ):
        """
        Creates a recurring-item

        :param conn: Connection-Object

        :param recurring_id: ID of the recurring
        :param article_id: ID of the article, sets additionally the values
            from the article on creation
        :param unit: Unit
        :param quantity: Quantity
        :param unit_price: Price per unit
        :param tax_name: Name of the tax
        :param tax_rate: rate of taxation
        :param title: Title
        :param description: Description
        :param reduction: Reduction (absolute or percent: 10/10%)
        """

        # XML
        xml = _recurring_item_xml(
            recurring_id = recurring_id,
            article_id = article_id,
            unit = unit,
            quantity = quantity,
            unit_price = unit_price,
            tax_name = tax_name,
            tax_rate = tax_rate,
            title = title,
            description = description,
            reduction = reduction
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Recurring-Object
        recurring = cls(conn = conn)
        recurring.content_language = response.headers.get("content-language", None)
        recurring.load_from_xml(response.data)

        # Finished
        return recurring


    def edit(
        self,
        id = None,
        article_id = None,
        unit = None,
        quantity = None,
        unit_price = None,
        tax_name = None,
        tax_rate = None,
        title = None,
        description = None,
        reduction = None
    ):
        """
        Edit a recurring-item

        :param id: ID of the recurring-item

        :param article_id: ID of the article, sets additionally the values
            from the article on creation
        :param unit: Unit
        :param quantity: Quantity
        :param unit_price: Price per unit
        :param tax_name: Name of the tax
        :param tax_rate: rate of taxation
        :param title: Title
        :param description: Description
        :param reduction: Reduction (absolute or percent: 10/10%)
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _recurring_item_xml(
            article_id = article_id,
            unit = unit,
            quantity = quantity,
            unit_price = unit_price,
            tax_name = tax_name,
            tax_rate = tax_rate,
            title = title,
            description = description,
            reduction = reduction
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


class RecurringItems(list):

    def __init__(self, conn):
        """
        RecurringItems-List

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

        :param recurring_id: ID of the recurring (mandatory) or a list of IDs.
            If list with IDs given: The result contains the recurring-items of
            many recurrings. Be careful: Too many recurring IDs can produce to
            large responses or to large SQL statements.
            My recommendation: 10-50 recurring IDs at one time.

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
        url = Url(path = "/api/recurring-items")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameter
        if isinstance(recurring_id, (list, tuple)):
            recurring_id = ",".join(str(id) for id in set(recurring_id))

        url.query["recurring_id"] = recurring_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        recurring_items_etree = ET.fromstring(response.data)

        self.per_page = int(recurring_items_etree.attrib.get("per_page", "100"))
        self.total = int(recurring_items_etree.attrib.get("total", "0"))
        self.page = int(recurring_items_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all items
        for recurring_item_etree in recurring_items_etree:
            self.append(
                RecurringItem(conn = self.conn, recurring_item_etree = recurring_item_etree)
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


class RecurringItemsIterator(ItemsIterator):
    """
    Iterates over all found recurrings
    """

    def __init__(self, conn, per_page = 30):
        """
        RecurringItemsIterator
        """

        self.conn = conn
        self.items = RecurringItems(self.conn)
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

        :param recurring_id: ID of the recurring (mandatory) or a list of IDs.
            If list with IDs given: The result contains the recurring-items of
            many recurrings. Be careful: To many recurring IDs can produce to
            large responses or to large SQL statements.
            My recommendation: 10-50 recurring IDs at one time.
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


