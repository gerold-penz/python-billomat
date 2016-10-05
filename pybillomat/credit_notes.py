#!/usr/bin/env python
# coding: utf-8
"""
Credit-Notes

- English API-Description: http://www.billomat.com/en/api/credit-notes/
- Deutsche API-Beschreibung: http://www.billomat.com/api/gutschriften/
"""

import datetime
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
import errors
from _items_base import Item, ItemsIterator


def _credit_note_xml(
    client_id = None,  # int
    contact_id = None,  # int
    address = None,
    number_pre = None,
    number = None,  # int
    number_length = None,  # int
    date = None,  # date
    title = None,
    label = None,
    intro = None,
    note = None,
    reduction = None,
    currency_code = None,
    net_gross = None,
    quote = None,  # float
    invoice_id = None  # int
):
    """
    Creates the XML to add or edit a credit note
    """

    integer_field_names = [
        "client_id",
        "contact_id",
        "number",
        "number_length",
        "invoice_id",
    ]
    date_or_string_fieldnames = [
    ]
    date_fieldnames = [
        "date",
    ]
    float_fieldnames = [
        "quote",
    ]
    string_fieldnames = [
        "address",
        "number_pre",
        "title",
        "label",
        "intro",
        "note",
        "reduction",
        "currency_code",
        "net_gross",
    ]

    credit_note_tag = ET.Element("credit-note")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            credit_note_tag.append(new_tag)

    # Date or string fields
    for field_name in date_or_string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            if isinstance(value, datetime.date):
                new_tag.text = value.isoformat()
            else:
                new_tag.text = unicode(value)
            credit_note_tag.append(new_tag)

    # Date fields
    for field_name in date_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = value.isoformat()
            credit_note_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            credit_note_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            credit_note_tag.append(new_tag)

    xml = ET.tostring(credit_note_tag)

    # Finished
    return xml


class CreditNote(Item):

    base_path = u"/api/credit-notes"


    def __init__(self, conn, id = None, credit_note_etree = None):
        """
        CreditNote

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # integer
        self.client_id = None  # integer
        self.contact_id = None  # integer
        self.created = None  # datetime
        self.credit_note_number = None
        self.number = None  # integer
        self.number_pre = None
        self.status = None
        self.date = None  # date
        self.address = None
        self.title = None
        self.label = None
        self.intro = None
        self.note = None
        self.total_gross = None  # float
        self.total_net = None  # float
        self.net_gross = None
        self.reduction = None
        self.total_gross_unreduced = None  # float
        self.total_net_unreduced = None  # float
        self.currency_code = None
        self.quote = None  # float
        self.invoice_id = None  # ID der korrigierten Rechnung
        self.taxes = None  # array

        if credit_note_etree is not None:
            self.load_from_etree(credit_note_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        client_id = None,  # int
        contact_id = None,  # int
        address = None,
        number_pre = None,
        number = None,  # int
        number_length = None,  # int
        date = None,  # date
        title = None,
        label = None,
        intro = None,
        note = None,
        reduction = None,
        currency_code = None,
        net_gross = None,
        quote = None,  # float
        invoice_id = None  # int
        # credit_note_items = None
    ):
        """
        Creates a credit note

        :param conn: Connection-Object
        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param address: the address
        :param number_pre: credit note number prefix
        :param number: serial number
        :param number_length: Minimum length of the credit note number
            (to be filled with leading zeros)
        :param date: Credit-note date
        :param title: Document title; Let it empty to use the default value
            from settings
        :param label: Label text to describe the project
        :param intro: Introductory text
        :param note: Explanatory notes
        :param reduction: Reduction (absolute or percent: 10/10%)
        :param currency_code: Currency; ISO currency code
        :param net_gross: Price basis (gross or net prices)
        :param quote: Currency quote (for conversion into standard currency)
        :param invoice_id: The ID of the invoice, if the credit note was
            created from an invoice.
        # :param invoice_items: List with CreditNoteItem-Objects
        """

        # XML
        xml = _credit_note_xml(
            client_id = client_id,  # int
            contact_id = contact_id,  # int
            address = address,
            number_pre = number_pre,
            number = number,  # int
            number_length = number_length,  # int
            date = date,  # date
            title = title,
            label = label,
            intro = intro,
            note = note,
            reduction = reduction,
            currency_code = currency_code,
            net_gross = net_gross,
            quote = quote,  # float
            invoice_id = invoice_id  # int
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
        client_id = None,  # int
        contact_id = None,  # int
        address = None,
        number_pre = None,
        number = None,  # int
        number_length = None,  # int
        date = None,  # date
        title = None,
        label = None,
        intro = None,
        note = None,
        reduction = None,
        currency_code = None,
        net_gross = None,
        quote = None,  # float
        invoice_id = None  # int
    ):
        """
        Edit an invoice

        :param id: ID of the invoice
        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param address: the address
        :param number_pre: credit note number prefix
        :param number: serial number
        :param number_length: Minimum length of the credit note number
            (to be filled with leading zeros)
        :param date: Credit-note date
        :param title: Document title; Let it empty to use the default value
            from settings
        :param label: Label text to describe the project
        :param intro: Introductory text
        :param note: Explanatory notes
        :param reduction: Reduction (absolute or percent: 10/10%)
        :param currency_code: Currency; ISO currency code
        :param net_gross: Price basis (gross or net prices)
        :param quote: Currency quote (for conversion into standard currency)
        :param invoice_id: The ID of the invoice, if the credit note was
            created from an invoice.
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _credit_note_xml(
            client_id = client_id,  # int
            contact_id = contact_id,  # int
            address = address,
            number_pre = number_pre,
            number = number,  # int
            number_length = number_length,  # int
            date = date,  # date
            title = title,
            label = label,
            intro = intro,
            note = note,
            reduction = reduction,
            currency_code = currency_code,
            net_gross = net_gross,
            quote = quote,  # float
            invoice_id = invoice_id  # int
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


class CreditNotes(list):

    def __init__(self, conn):
        """
        CreditNotes-List

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
        client_id = None,
        contact_id = None,
        credit_note_number = None,
        status = None,
        from_date = None,
        to_date = None,
        label = None,
        intro = None,
        note = None,
        tags = None,
        article_id = None,

        order_by = None,
        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with CreditNote-objects

        If no search criteria given --> all credit notes will returned (REALLY ALL!).

        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param credit_note_number: credit note number
        :param status: Status (DRAFT, OPEN, PAID).
            More than one statuses could be given as a comma separated list.
            Theses statuses will be logically OR-connected.
        :param from_date: (originaly: "from") Only show credit notes since this
            date (format YYYY-MM-DD)
        :param to_date: (originaly: "to") Only show credit notes up to this
            date (format YYYY-MM-DD)
        :param label: Free text search in label text
        :param intro: Free text search in introductory text
        :param note: Free text search in explanatory notes
        :param tags: Comma seperated list of tags
        :param article_id: ID of an article

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        :param allow_empty_filter: If `True`, every filter-parameter may be empty.
            So, all credit notes will returned. !!! EVERY CREDIT NOTE !!!
        """
        
        # Check empty filter
        if not allow_empty_filter:
            if not any([
                client_id,
                contact_id,
                credit_note_number,
                status,
                from_date,
                to_date,
                label,
                intro,
                note,
                tags,
                article_id,
            ]):
                raise errors.EmptyFilterError()

        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Url and system-parameters
        url = Url(path = CreditNote.base_path)
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameters
        if client_id:
            url.query["client_id"] = client_id
        if contact_id:
            url.query["contact_id"] = contact_id
        if credit_note_number:
            url.query["credit_note_number"] = credit_note_number
        if status:
            url.query["status"] = status
        if from_date:
            url.query["from"] = from_date
        if to_date:
            url.query["to"] = to_date
        if label:
            url.query["label"] = label
        if intro:
            url.query["intro"] = intro
        if note:
            url.query["note"] = note
        if tags:
            url.query["tags"] = tags
        if article_id:
            url.query["article_id"] = article_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        credit_notes_etree = ET.fromstring(response.data)

        self.per_page = int(credit_notes_etree.attrib.get("per_page", "100"))
        self.total = int(credit_notes_etree.attrib.get("total", "0"))
        self.page = int(credit_notes_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all credit notes
        for credit_note_etree in credit_notes_etree:
            self.append(CreditNote(conn = self.conn, credit_note_etree = credit_note_etree))

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                client_id = client_id,
                contact_id = contact_id,
                credit_note_number = credit_note_number,
                status = status,
                from_date = from_date,
                to_date = to_date,
                label = label,
                intro = intro,
                note = note,
                tags = tags,
                article_id = article_id,

                order_by = order_by,
                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class CreditNotesIterator(ItemsIterator):
    """
    Iterates over all found credit notes
    """

    def __init__(self, conn, per_page = 30):
        """
        CreditNotesIterator
        """

        self.conn = conn
        self.items = CreditNotes(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            client_id = None,
            contact_id = None,
            credit_note_number = None,
            status = None,
            payment_type = None,
            from_date = None,
            to_date = None,
            label = None,
            intro = None,
            note = None,
            tags = None,
            article_id = None,
            order_by = None,
        )


    def search(
        self,
        client_id = None,
        contact_id = None,
        credit_note_number = None,
        status = None,
        from_date = None,
        to_date = None,
        label = None,
        intro = None,
        note = None,
        tags = None,
        article_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.client_id = client_id
        self.search_params.contact_id = contact_id
        self.search_params.credit_note_number = credit_note_number
        self.search_params.status = status
        self.search_params.from_date = from_date
        self.search_params.to_date = to_date
        self.search_params.label = label
        self.search_params.intro = intro
        self.search_params.note = note
        self.search_params.tags = tags
        self.search_params.article_id = article_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            client_id = self.search_params.client_id,
            contact_id = self.search_params.contact_id,
            credit_note_number = self.search_params.credit_note_number,
            status = self.search_params.status,
            from_date = self.search_params.from_date,
            to_date = self.search_params.to_date,
            label = self.search_params.label,
            intro = self.search_params.intro,
            note = self.search_params.note,
            tags = self.search_params.tags,
            article_id = self.search_params.article_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )

