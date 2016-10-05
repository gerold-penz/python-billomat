#!/usr/bin/env python
# coding: utf-8
"""
Credit Note Items

- English API-Description: http://www.billomat.com/en/api/credit-notes/items/
- Deutsche API-Beschreibung: http://www.billomat.com/api/gutschriften/positionen/
"""


import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _credit_note_item_xml(
    credit_note_id = None,  # int
    article_id = None,  # int
    unit = None,
    quantity = None,  # float
    unit_price = None,  # float
    tax_name = None,
    tax_rate = None,  # float
    title = None,
    description = None,
    reduction = None
):
    """
    Creates the XML to add or edit an credit note item
    """

    integer_field_names = [
        "credit_note_id",
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

    credit_note_item_tag = ET.Element("credit-note-item")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            credit_note_item_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            credit_note_item_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            credit_note_item_tag.append(new_tag)

    xml = ET.tostring(credit_note_item_tag)

    # Finished
    return xml


class CreditNoteItem(Item):

    base_path = u"/api/credit-note-items"


    def __init__(self, conn, id = None, credit_note_item_etree = None):
        """
        Credit Note Item

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.article_id = None
        self.credit_note_id = None  # integer
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

        if credit_note_item_etree is not None:
            self.load_from_etree(credit_note_item_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        credit_note_id = None,
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
        Creates a credit note item

        :param conn: Connection-Object

        :param credit_note_id: ID of the credit note
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
        xml = _credit_note_item_xml(
            credit_note_id = credit_note_id,
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

        # Create CreditNote-Object
        credit_note = cls(conn = conn)
        credit_note.content_language = response.headers.get("content-language", None)
        credit_note.load_from_xml(response.data)

        # Finished
        return credit_note


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
        Edit a credit note item

        :param id: ID of the credit note item

        :param article_id: ID of the article, sets additionally the values
            from the article on creation
        :param unit: Unit
        :param quantity: Quantity
        :param unit_price: Price per unit
        :param tax_name: Name of the tax
        :param tax_rate: Rate of taxation
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
        xml = _credit_note_item_xml(
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


class CreditNoteItems(list):

    def __init__(self, conn):
        """
        CreditNoteItems-List

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
        credit_note_id = None,

        order_by = None,
        fetch_all = False,
        keep_old_items = False,
        page = 1,
        per_page = None,

        credit_note_ids = None
    ):
        """
        Fills the list with CreditNoteItem-objects

        :param credit_note_id: ID of the credit note (mandatory) or a list of IDs.
            If list with IDs given: The result contains the credit note items of
            many credit notes. Be careful: Too many credit note IDs can produce to
            large responses or to large SQL statements.
            My recommendation: 10-50 credit note IDs at one time.

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.
        """

        # Check empty param
        if not credit_note_id:
            raise errors.EmptyFilterError()

        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Url and system-parameters
        url = Url(path = CreditNoteItem.base_path)
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameter
        if isinstance(credit_note_id, (list, tuple)):
            credit_note_id = ",".join(str(id) for id in set(credit_note_id))

        url.query["credit_note_id"] = credit_note_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        credit_note_items_etree = ET.fromstring(response.data)

        self.per_page = int(credit_note_items_etree.attrib.get("per_page", "100"))
        self.total = int(credit_note_items_etree.attrib.get("total", "0"))
        self.page = int(credit_note_items_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all items
        for credit_note_item_etree in credit_note_items_etree:
            self.append(
                CreditNoteItem(conn = self.conn, credit_note_item_etree = credit_note_item_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                credit_note_id = credit_note_id,

                order_by = order_by,
                fetch_all = fetch_all,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class CreditNoteItemsIterator(ItemsIterator):
    """
    Iterates over all found credit notes
    """

    def __init__(self, conn, per_page = 30):
        """
        CreditNoteItemsIterator
        """

        self.conn = conn
        self.items = CreditNoteItems(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            credit_note_id = None,
            order_by = None
        )


    def search(
        self,
        credit_note_id = None,
        order_by = None
    ):
        """
        Search

        :param credit_note_id: ID of the credit note (mandatory) or a list of IDs.
            If list with IDs given: The result contains the credit note items of
            many credit notes. Be careful: To many credit note IDs can produce to
            large responses or to large SQL statements.
            My recommendation: 10-50 credit note IDs at one time.
        """

        # Params
        self.search_params.credit_note_id = credit_note_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            credit_note_id = self.search_params.credit_note_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


