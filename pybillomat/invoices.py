#!/usr/bin/env python
# coding: utf-8
"""
Clients

- English API-Description: http://www.billomat.com/en/api/invoices
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/rechnungen
"""

import datetime
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
import errors


class Invoice(Bunch):

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
        self.due_date = None  # date
        self.due_days = None  # integer
        self.address = None
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
        self.invoice_id = None
        self.offer_id = None
        self.confirmation_id = None
        self.recurring_id = None
        self.taxes = None  # array
        self.payment_types = None

        if not invoice_etree is None:
            self.load_from_etree(invoice_etree)


    def load_from_etree(self, etree_element):
        """
        Loads data from Element-Tree
        """

        for item in etree_element:

            # Get data
            isinstance(item, ET.Element)
            tag = item.tag
            type = item.attrib.get("type")
            text = item.text

            if not text is None:
                if type == "integer":
                    setattr(self, tag, int(text))
                elif type == "datetime":
                    # <created type="datetime">2011-10-04T17:40:00+02:00</created>
                    dt = datetime.datetime.strptime(text[:19], "%Y-%m-%dT%H:%M:%S")
                    setattr(self, tag, dt)
                elif type == "date":
                    # <date type="date">2009-10-14</date>
                    d = datetime.date(*[int(item)for item in text.strip().split("-")])
                    setattr(self, tag, d)
                elif type == "float":
                    setattr(self, tag, float(text))
                else:
                    if isinstance(text, str):
                        text = text.decode("utf-8")
                    setattr(self, tag, text)


    def load_from_xml(self, xml_string):
        """
        Loads data from XML-String
        """

        # Parse XML
        root = ET.fromstring(xml_string)

        # Load
        self.load_from_etree(root)


    def load(self, id = None):
        """
        Loads the invoice-data from server
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # Path
        path = "/api/invoices/{id}".format(id = self.id)

        # Fetch data
        response = self.conn.get(path = path)
        if not response.status == 200:
            raise errors.InvoiceNotFoundError(unicode(self.id))

        # Fill in data from XML
        self.load_from_xml(response.data)
        self.content_language = response.headers.get("content-language", None)


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

        self.per_page = int(invoices_etree.attrib.get("per_page", "0"))
        self.total = int(invoices_etree.attrib.get("total", "0"))
        self.page = int(invoices_etree.attrib.get("page", "1"))
        self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))

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

                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )





