#!/usr/bin/env python
# coding: utf-8
"""
Invoices

- English API-Description: http://www.billomat.com/en/api/invoices
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/rechnungen
"""

import datetime
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
import errors
from _items_base import Item, ItemsIterator


def _invoice_xml(
    client_id = None,
    contact_id = None,
    address = None,
    number_pre = None,
    number = None,
    number_length = None,
    date = None,
    supply_date = None,
    supply_date_type = None,
    due_date = None,
    discount_rate = None,
    discount_days = None,
    title = None,
    label = None,
    intro = None,
    note = None,
    reduction = None,
    currency_code = None,
    net_gross = None,
    quote = None,
    payment_types = None,
    invoice_id = None,
    offer_id = None,
    confirmation_id = None,
    recurring_id = None,
):
    """
    Creates the XML to add or edit an invoice
    """

    integer_field_names = [
        "client_id",
        "contact_id",
        "discount_rate",
        "discount_days",
        "offer_id",
        "confirmation_id",
        "number",
        "number_length",
        "invoice_id",
        "recurring_id",
    ]
    date_or_string_fieldnames = [
        "supply_date",
    ]
    date_fieldnames = [
        "date",
        "due_date"
    ]
    float_fieldnames = [
        "quote",
    ]
    string_fieldnames = [
        "title",
        "address",
        "number_pre",
        "supply_date_type",
        "label",
        "intro",
        "note",
        "currency_code",
        "reduction",
        "net_gross",
        "payment_types",
    ]

    invoice_tag = ET.Element("invoice")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            invoice_tag.append(new_tag)

    # Date or string fields
    for field_name in date_or_string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            if isinstance(value, datetime.date):
                new_tag.text = value.isoformat()
            else:
                new_tag.text = unicode(value)
            invoice_tag.append(new_tag)

    # Date fields
    for field_name in date_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = value.isoformat()
            invoice_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            invoice_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            invoice_tag.append(new_tag)

    xml = ET.tostring(invoice_tag)

    # Finished
    return xml



class Invoice(Item):

    base_path = u"/api/invoices"


    def __init__(self, conn, id = None, invoice_etree = None):
        """
        Invoice

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # integer
        self.client_id = None  # integer
        self.contact_id = None  # integer
        self.created = None  # datetime
        self.invoice_number = None
        self.number = None  # integer
        self.number_pre = None
        self.status = None
        self.date = None  # date
        self.supply_date = None
        self.supply_date_type = None
        #     SUPPLY_DATE (Leistungsdatum als Datum)
        #     DELIVERY_DATE (Lieferdatum als Datum)
        #     SUPPLY_TEXT (Leistungsdatum als Freitext)
        #     DELIVERY_TEXT (Lieferdatum als Freitext)
        self.due_date = None  # date
        self.due_days = None  # integer
        self.address = None  # Pass an empty value to use the current customer address.
        self.discount_rate = None  # float
        self.discount_date = None  # date
        self.discount_days = None  # integer
        self.discount_amount = None  # float
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
        self.paid_amount = None  # float
        self.open_amount = None  # float
        self.currency_code = None
        self.quote = None  # float
        self.invoice_id = None  # ID der korrigierten Rechnung
        self.offer_id = None
        self.confirmation_id = None
        self.recurring_id = None
        self.taxes = None  # array
        self.payment_types = None
        #    INVOICE_CORRECTION (Korrekturrechnung)
        #    CREDIT_NOTE (Gutschrift)
        #    BANK_CARD (Bankkarte)
        #    BANK_TRANSFER (Überweisung)
        #    DEBIT (Lastschrift)
        #    CASH (Bar)
        #    CHECK (Scheck)
        #    PAYPAL (Paypal)
        #    CREDIT_CARD (Kreditkarte)
        #    COUPON (Gutschein)
        #    MISC (Sonstiges)

        if invoice_etree is not None:
            self.load_from_etree(invoice_etree)
        elif id is not None:
            self.load()


    def complete(self, template_id = None):
        """
        Closes a statement in the draft status (DRAFT) from.
        The status of open (OPEN) or overdue (Overdue) is set and
        a PDF is generated and stored in the file system.
        """

        # Path
        path = "/api/invoices/{id}/complete".format(id = self.id)

        # XML
        complete_tag = ET.Element("complete")
        if template_id:
            template_id_tag = ET.Element("template_id")
            template_id_tag.text = str(template_id)
            complete_tag.append(template_id_tag)
        xml = ET.tostring(complete_tag)

        # Send PUT-request
        response = self.conn.put(path = path, body = xml)

        if response.status != 200:
            # Parse response
            error_text_list = []
            for error in ET.fromstring(response.data):
                error_text_list.append(error.text)

            # Raise Error
            raise errors.BillomatError("\n".join(error_text_list))


    def send(
        self,
        from_address = None,
        to_address = None,
        cc_address = None,
        bcc_address = None,
        subject = None,
        body = None,
        filename = None,
        # attachments = None
    ):
        """
        Sends the invoice per e-mail to the customer

        :param from_address: (originally: from) Sender
        :param to_address: (originally: recepients)
        :param cc_address: (originally: recepients)
        :param bcc_address: (originally: recepients)
        :param subject: Subject of the e-mail (may include placeholders)
        :param body: Text of the e-mail (may include placeholders)
        :param filename: Name of the PDF file (without .pdf)
        # :param attachments: List with Dictionaries::
        #
        #     [
        #         {
        #             "filename": "<Filename>",
        #             "mimetype": "<MimeType>",
        #             "base64file": "<Base64EncodedFile>"
        #         },
        #         ...
        #     ]
        """

        # Path
        path = "{base_path}/{id}/email".format(
            base_path = self.base_path,
            id = self.id
        )

        # XML
        email_tag = ET.Element("email")

        # From
        if from_address:
            from_tag = ET.Element("from")
            from_tag.text = from_address
            email_tag.append(from_tag)

        # Recipients
        if to_address or cc_address or bcc_address:
            recipients_tag = ET.Element("recipients")
            email_tag.append(recipients_tag)

            # To
            if to_address:
                to_tag = ET.Element("to")
                to_tag.text = to_address
                recipients_tag.append(to_tag)

            # Cc
            if cc_address:
                cc_tag = ET.Element("cc")
                cc_tag.text = cc_address
                recipients_tag.append(cc_tag)

            # Bcc
            if bcc_address:
                bcc_tag = ET.Element("bcc")
                bcc_tag.text = bcc_address
                recipients_tag.append(bcc_tag)

        # Subject
        if subject:
            subject_tag = ET.Element("subject")
            subject_tag.text = subject
            email_tag.append(subject_tag)

        # Body
        if body:
            body_tag = ET.Element("body")
            body_tag.text = body
            email_tag.append(body_tag)

        # Filename
        if filename:
            filename_tag = ET.Element("filename")
            filename_tag.text = filename
            filename_tag.append(filename_tag)

        # ToDo: Attachments

        xml = ET.tostring(email_tag)

        # Send POST-request
        response = self.conn.post(path = path, body = xml)

        if response.status != 200:
            # Parse response
            error_text_list = []
            for error in ET.fromstring(response.data):
                error_text_list.append(error.text)

            # Raise Error
            raise errors.BillomatError("\n".join(error_text_list))


    @classmethod
    def create(
        cls,
        conn,
        client_id = None,
        contact_id = None,
        address = None,
        number_pre = None,
        number = None,
        number_length = None,
        date = None,
        supply_date = None,
        supply_date_type = None,
        due_date = None,
        discount_rate = None,
        discount_days = None,
        title = None,
        label = None,
        intro = None,
        note = None,
        reduction = None,
        currency_code = None,
        net_gross = None,
        quote = None,
        payment_types = None,
        invoice_id = None,
        offer_id = None,
        confirmation_id = None,
        recurring_id = None,
        # invoice_items = None
    ):
        """
        Creates an invoice

        :param conn: Connection-Object
        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param address: the address
        :param number_pre: invoice number prefix
        :param number: serial number
        :param number_length: Minimum length of the invoice number
            (to be filled with leading zeros)
        :param date: Invoice date
        :param supply_date: supply/delivery date; MIXED (DATE/ALNUM)
        :param supply_date_type: type or supply/delivery date; ALNUM (
            "SUPPLY_DATE", "DELIVERY_DATE", "SUPPLY_TEXT", "DELIVERY_TEXT")
        :param due_date: due date
        :param discount_rate: Cash discount
        :param discount_days: Cash discount date
        :param title: Document title; Let it empty to use the default value
            from settings: "Invoice [Invoice.invoice_number]"
        :param label: Label text to describe the project
        :param intro: Introductory text
        :param note: Explanatory notes
        :param reduction: Reduction (absolute or percent: 10/10%)
        :param currency_code: Currency; ISO currency code
        :param net_gross: Price basis (gross or net prices)
        :param quote: Currency quote (for conversion into standard currency)
        :param payment_types: List (separated by comma) of all accepted
            payment types.
        :param invoice_id: The ID of the corrected invoice, if it is an
            invoice correction.
        :param offer_id: The ID of the estimate, if the invoice was created
            from an estimate.
        :param confirmation_id: The ID of the confirmation, if the invoice was
            created from a confirmation.
        :param recurring_id: The ID of the recurring, if the invoice was
            created from a recurring.
        # :param invoice_items: List with InvoiceItem-Objects
        """

        # XML
        xml = _invoice_xml(
            client_id = client_id,
            contact_id = contact_id,
            address = address,
            number_pre = number_pre,
            number = number,
            number_length = number_length,
            date = date,
            supply_date = supply_date,
            supply_date_type = supply_date_type,
            due_date = due_date,
            discount_rate = discount_rate,
            discount_days = discount_days,
            title = title,
            label = label,
            intro = intro,
            note = note,
            reduction = reduction,
            currency_code = currency_code,
            net_gross = net_gross,
            quote = quote,
            payment_types = payment_types,
            invoice_id = invoice_id,
            offer_id = offer_id,
            confirmation_id = confirmation_id,
            recurring_id = recurring_id
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
        client_id = None,
        contact_id = None,
        address = None,
        number_pre = None,
        number = None,
        number_length = None,
        date = None,
        supply_date = None,
        supply_date_type = None,
        due_date = None,
        discount_rate = None,
        discount_days = None,
        title = None,
        label = None,
        intro = None,
        note = None,
        reduction = None,
        currency_code = None,
        net_gross = None,
        quote = None,
        payment_types = None,
        invoice_id = None,
        offer_id = None,
        confirmation_id = None,
        recurring_id = None,
    ):
        """
        Edit an invoice

        :param id: ID of the invoice
        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param address: the address
        :param number_pre: invoice number prefix
        :param number: serial number
        :param number_length: Minimum length of the invoice number
            (to be filled with leading zeros)
        :param date: Invoice date
        :param supply_date: supply/delivery date; MIXED (DATE/ALNUM)
        :param supply_date_type: type or supply/delivery date; ALNUM (
            "SUPPLY_DATE", "DELIVERY_DATE", "SUPPLY_TEXT", "DELIVERY_TEXT")
        :param due_date: due date
        :param discount_rate: Cash discount
        :param discount_days: Cash discount date
        :param title: Document title; Let it empty to use the default value
            from settings: "Invoice [Invoice.invoice_number]"
        :param label: Label text to describe the project
        :param intro: Introductory text
        :param note: Explanatory notes
        :param reduction: Reduction (absolute or percent: 10/10%)
        :param currency_code: Currency; ISO currency code
        :param net_gross: Price basis (gross or net prices)
        :param quote: Currency quote (for conversion into standard currency)
        :param payment_types: List (separated by comma) of all accepted
            payment types.
        :param invoice_id: The ID of the corrected invoice, if it is an
            invoice correction.
        :param offer_id: The ID of the estimate, if the invoice was created
            from an estimate.
        :param confirmation_id: The ID of the confirmation, if the invoice was
            created from a confirmation.
        :param recurring_id: The ID of the recurring, if the invoice was
            created from a recurring.
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _invoice_xml(
            client_id = client_id,
            contact_id = contact_id,
            address = address,
            number_pre = number_pre,
            number = number,
            number_length = number_length,
            date = date,
            supply_date = supply_date,
            supply_date_type = supply_date_type,
            due_date = due_date,
            discount_rate = discount_rate,
            discount_days = discount_days,
            title = title,
            label = label,
            intro = intro,
            note = note,
            reduction = reduction,
            currency_code = currency_code,
            net_gross = net_gross,
            quote = quote,
            payment_types = payment_types,
            invoice_id = invoice_id,
            offer_id = offer_id,
            confirmation_id = confirmation_id,
            recurring_id = recurring_id
        )

        # Path
        path = "/api/invoices/{id}".format(id = self.id)

        # Send PUT-request
        response = self.conn.put(path = path, body = xml)
        if response.status != 200:  # Edited
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))


    # def get_tags(self):
    #     """
    #     Gibt eine Liste mit Schlagworten der Rechnung zurück
    #     """
    #
    #     # Parameters
    #     if not self.id:
    #         raise errors.NoIdError()
    #     ...


class Invoices(list):

    def __init__(self, conn):
        """
        Invoices-List

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
        invoice_number = None,
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
        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with Invoice-objects

        If no search criteria given --> all invoices will returned (REALLY ALL!).

        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param invoice_number: invoice number
        :param status: Status (DRAFT, OPEN, PAID, OVERDUE, CANCELED).
            More than one statuses could be given as a comma separated list.
            Theses statuses will be logically OR-connected.
        :param payment_type: Payment Type (eg. CASH, BANK_TRANSFER, PAYPAL, ...).
            More than one payment type could be given as a comma separated list.
            Theses payment types will be logically OR-connected.
            You can find a overview of all payment types at API documentation
            of payments.
        :param from_date: (originaly: "from") Only show invoices since this
            date (format YYYY-MM-DD)
        :param to_date: (originaly: "to") Only show invoices up to this
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
            So, all invoices will returned. !!! EVERY INVOICE !!!
        """
        
        # Check empty filter
        if not allow_empty_filter:
            if not any([
                client_id,
                contact_id,
                invoice_number,
                status,
                payment_type,
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
        url = Url(path = "/api/invoices")
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
        if invoice_number:
            url.query["invoice_number"] = invoice_number
        if status:
            url.query["status"] = status
        if payment_type:
            url.query["payment_type"] = payment_type
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
        invoices_etree = ET.fromstring(response.data)

        self.per_page = int(invoices_etree.attrib.get("per_page", "100"))
        self.total = int(invoices_etree.attrib.get("total", "0"))
        self.page = int(invoices_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all invoices
        for invoice_etree in invoices_etree:
            self.append(Invoice(conn = self.conn, invoice_etree = invoice_etree))

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                client_id = client_id,
                contact_id = contact_id,
                invoice_number = invoice_number,
                status = status,
                payment_type = payment_type,
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


class InvoicesIterator(ItemsIterator):
    """
    Iterates over all found invoices
    """

    def __init__(self, conn, per_page = 30):
        """
        InvoicesIterator
        """

        self.conn = conn
        self.items = Invoices(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            client_id = None,
            contact_id = None,
            invoice_number = None,
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
        invoice_number = None,
        status = None,
        payment_type = None,
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
        self.search_params.invoice_number = invoice_number
        self.search_params.status = status
        self.search_params.payment_type = payment_type
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
            invoice_number = self.search_params.invoice_number,
            status = self.search_params.status,
            payment_type = self.search_params.payment_type,
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


