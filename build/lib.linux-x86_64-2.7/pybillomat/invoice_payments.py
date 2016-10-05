#!/usr/bin/env python
# coding: utf-8
"""
Invoice-Payments

- English API-Description: http://www.billomat.com/en/api/invoices/payments
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/rechnungen/zahlungen
"""

import urllib3
import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _invoice_payment_xml(
    invoice_id = None,
    date = None,
    amount = None,
    comment = None,
    type = None,
    mark_invoice_as_paid = None
):
    """
    Creates the XML to add or edit a recurring-item
    """

    integer_fieldnames = [
        "invoice_id",
    ]
    date_fieldnames = [
        "date",
    ]
    float_fieldnames = [
        "amount",
    ]
    boolean_fieldnames = [
        "mark_invoice_as_paid",
    ]
    string_fieldnames = [
        "type",
        "comment"
    ]

    invoice_payment_tag = ET.Element("recurring-item")

    # Integer Fields
    for field_name in integer_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            invoice_payment_tag.append(new_tag)

    # Date fields
    for field_name in date_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = value.isoformat()
            invoice_payment_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            invoice_payment_tag.append(new_tag)

    # Boolean Fields
    for field_name in boolean_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = "1" if value else "0"
            invoice_payment_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            invoice_payment_tag.append(new_tag)

    xml = ET.tostring(invoice_payment_tag)

    # Finished
    return xml


class InvoicePayment(Item):

    base_path = u"/api/invoice-payments"


    def __init__(self, conn, id = None, payment_etree = None):
        """
        InvoicePayment

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # Integer
        self.created = None  # Datetime
        self.invoice_id = None  # Not always filled
        self.user_id = None  # Integer
        self.date = None  # Date
        self.amount = None  # Float
        self.comment = None
        self.type = None

        if payment_etree is not None:
            self.load_from_etree(payment_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        invoice_id,
        date = None,
        amount = None,
        comment = None,
        type = None,
        mark_invoice_as_paid = None
    ):
        """
        Creates one invoice-payment

        :param conn: Connection-Object; Mandatory
        :param invoice_id: ID of an invoice
        :param date: Date of payment; Default: today
        :param amount: Payed ammount; Mandatory
        :param comment: Comment text
        :param type: Payment type;
            Possible values:

            - CREDIT_NOTE
            - BANK_CARD
            - BANK_TRANSFER
            - DEBIT
            - CASH
            - CHECK
            - PAYPAL
            - CREDIT_CARD
            - COUPON
            - MISC

        :param mark_invoice_as_paid: Indicates whether the associated invoice
            should be marked as paid (set status to PAID).
        """

        assert invoice_id
        assert amount is not None

        # XML
        xml = _invoice_payment_xml(
            invoice_id = invoice_id,
            date = date,
            amount = amount,
            comment = comment,
            type = type,
            mark_invoice_as_paid = mark_invoice_as_paid
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create InvoicePayment-Object
        invoice_payment = cls(conn = conn)
        invoice_payment.content_language = response.headers.get("content-language", None)
        invoice_payment.load_from_xml(response.data)

        # Finished
        return invoice_payment


class InvoicePayments(list):

    def __init__(self, conn):
        """
        InvoicePayments-List

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
        from_date = None,
        to_date = None,
        type = None,
        user_id = None,
        order_by = None,

        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the (internal) list with InvoicePayment-objects

        If no search criteria given --> all payments will returned (REALLY ALL!).

        :param invoice_id: ID of the invoice

        :param from_date: Original "from"; Only payments since this date

        :param to_date: Original "to"; Only payments up to this date

        :param type: Payment type (eg. CASH, BANK_TRANSFER, PAYPAL, ...).
            More than one payment type could be given as a comma separated list.
            Theses payment types will be logically OR-connected.

        :param user_id: ID of the user

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        :param allow_empty_filter: If `True`, every filter-parameter may be empty.
            All invoice-payments will returned. !!! EVERY !!!
        """

        # Check empty filter
        if not allow_empty_filter:
            if not any([
                invoice_id,
                from_date,
                to_date,
                type,
                user_id,
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
        url = Url(path = "/api/invoice-payments")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameters
        if invoice_id:
            url.query["invoice_id"] = invoice_id
        if from_date:
            url.query["from"] = from_date
        if to_date:
            url.query["to"] = to_date
        if type:
            url.query["type"] = type
        if user_id:
            url.query["user_id"] = user_id

        # Fetch data
        response = self.conn.get(path = str(url))
        if response.status != 200:
            # Check if "Unothorized" --> raise NotFoundError
            errors_etree = ET.fromstring(response.data)
            for error_etree in errors_etree:
                text = error_etree.text
                if text.lower() == "unauthorized":
                    raise errors.NotFoundError(
                        u"invoice_id: {invoice_id}".format(invoice_id = invoice_id)
                    )
            # Other Error
            raise errors.BillomatError(response.data)

        # No response (workaround for inconsistent gziped answer; DecodeError)
        try:
            if len(response.data) == 0:
                return
        except urllib3.exceptions.DecodeError:
            if response.headers.get("content-type", "").lower() != "application/xml":
                return
            else:
                raise

        # Parse XML
        payments_etree = ET.fromstring(response.data)

        self.per_page = int(payments_etree.attrib.get("per_page", "0"))
        self.total = int(payments_etree.attrib.get("total", "0"))
        self.page = int(payments_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all payments
        for payment_etree in payments_etree:
            self.append(
                InvoicePayment(conn = self.conn, payment_etree = payment_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                invoice_id = invoice_id,
                from_date = from_date,
                to_date = to_date,
                type = type,
                user_id = user_id,
                order_by = order_by,

                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class InvoicePaymentsIterator(ItemsIterator):
    """
    Iterates over all found payments
    """

    def __init__(self, conn, per_page = 100):
        """
        InvoicePaymentsIterator
        """

        self.conn = conn
        self.items = InvoicePayments(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            invoice_id = None,
            from_date = None,
            to_date = None,
            type = None,
            user_id = None,
            order_by = None,
        )


    def search(
        self,
        invoice_id = None,
        from_date = None,
        to_date = None,
        type = None,
        user_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.invoice_id = invoice_id
        self.search_params.from_date = from_date
        self.search_params.to_date = to_date
        self.search_params.type = type
        self.search_params.user_id = user_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            invoice_id = self.search_params.invoice_id,
            from_date = self.search_params.from_date,
            to_date = self.search_params.to_date,
            type = self.search_params.type,
            user_id = self.search_params.user_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )
