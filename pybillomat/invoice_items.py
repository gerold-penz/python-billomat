#!/usr/bin/env python
# coding: utf-8
"""
Invoice-Items

- English API-Description: http://www.billomat.com/en/api/invoices/items
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/rechnungen/positionen
"""


import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _invoice_item_xml(
    invoice_id = None,
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
    Creates the XML to add or edit a invoice-item
    """

    integer_field_names = [
        "invoice_id",
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

    invoice_item_tag = ET.Element("invoice-item")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            invoice_item_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            invoice_item_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            invoice_item_tag.append(new_tag)

    xml = ET.tostring(invoice_item_tag)

    # Finished
    return xml


class InvoiceItem(Item):

    base_path = u"/api/invoice-items"


    def __init__(self, conn, id = None, invoice_item_etree = None):
        """
        Invoice-Item

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.article_id = None
        self.invoice_id = None  # integer
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

        if invoice_item_etree is not None:
            self.load_from_etree(invoice_item_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        invoice_id = None,
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
        Creates a invoice-item

        :param conn: Connection-Object

        :param invoice_id: ID of the invoice
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
        xml = _invoice_item_xml(
            invoice_id = invoice_id,
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

        # Create Invoice-Object
        invoice = cls(conn = conn)
        invoice.content_language = response.headers.get("content-language", None)
        invoice.load_from_xml(response.data)

        # Finished
        return invoice


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
        Edit a invoice-item

        :param id: ID of the invoice-item

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
        xml = _invoice_item_xml(
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


class InvoiceItems(list):

    def __init__(self, conn):
        """
        InvoiceItems-List

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
        invoice_id = None,

        order_by = None,
        fetch_all = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with InvoiceItem-objects

        :param invoice_id: ID of the invoice (mandatory)

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        """

        # Check empty param
        if not invoice_id:
            raise errors.EmptyFilterError()

        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Url and system-parameters
        url = Url(path = "/api/invoice-items")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameter
        url.query["invoice_id"] = invoice_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        invoice_items_etree = ET.fromstring(response.data)

        self.per_page = int(invoice_items_etree.attrib.get("per_page", "100"))
        self.total = int(invoice_items_etree.attrib.get("total", "0"))
        self.page = int(invoice_items_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all items
        for invoice_item_etree in invoice_items_etree:
            self.append(
                InvoiceItem(conn = self.conn, invoice_item_etree = invoice_item_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                invoice_id = invoice_id,

                order_by = order_by,
                fetch_all = fetch_all,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class InvoiceItemsIterator(ItemsIterator):
    """
    Iterates over all found invoices
    """

    def __init__(self, conn, per_page = 30):
        """
        InvoiceItemsIterator
        """

        self.conn = conn
        self.items = InvoiceItems(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            invoice_id = None,
            order_by = None
        )


    def search(
        self,
        invoice_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.invoice_id = invoice_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            invoice_id = self.search_params.invoice_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


