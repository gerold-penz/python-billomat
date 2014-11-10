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
        path = "/api/invoices/{id}/email".format(id = self.id)

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

        self.per_page = int(invoices_etree.attrib.get("per_page", "100"))
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


class InvoicesIterator(object):
    """
    Iterates over all found invoices
    """

    def __init__(self, conn, per_page = 30):
        """
        InvoicesIterator
        """

        self.conn = conn
        self.invoices = Invoices(self.conn)
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

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.invoices.search(
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
            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


    def __len__(self):
        """
        Returns the count of found invoices
        """

        return self.invoices.total or 0


    def __iter__(self):
        """
        Iterate over all found items
        """

        for page in range(1, self.invoices.pages + 1):
            if not self.invoices.page == page:
                self.load_page(page = page)
            for invoice in self.invoices:
                yield invoice


    def __getitem__(self, key):
        """
        Returns the requested invoice from the pool of found invoices
        """

        # List-Ids
        all_list_ids = range(len(self))
        requested_list_ids = all_list_ids[key]
        is_list = isinstance(requested_list_ids, list)
        if not is_list:
            requested_list_ids = [requested_list_ids]

        result = []

        for list_id in requested_list_ids:

            # In welcher Seite befindet sich die gewünschte ID?
            for page_nr in range(1, self.invoices.pages + 1):
                max_list_id = (page_nr * self.invoices.per_page) - 1
                if list_id <= max_list_id:
                    page = page_nr
                    break
            else:
                raise AssertionError()

            # Load page if neccessary
            if not self.invoices.page == page:
                self.load_page(page = page)

            # Add equested invoice-object to result
            list_id_in_page = list_id - ((page - 1) * self.invoices.per_page)
            result.append(self.invoices[list_id_in_page])

        if is_list:
            return result
        else:
            return result[0]



