#!/usr/bin/env python
# coding: utf-8
"""
Recurrings (Abo-Rechnungen)

- English API-Description: http://www.billomat.com/en/api/recurrings
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/abo-rechnungen
"""


import datetime
import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url
from _tools import ItemsIterator


def _recurring_xml(
    client_id = None,
    contact_id = None,
    title = None,
    address = None,
    supply_date = None,
    supply_date_type = None,
    due_days = None,
    discount_rate = None,
    discount_days = None,
    name = None,
    label = None,
    intro = None,
    note = None,
    currency_code = None,
    reduction = None,
    net_gross = None,
    quote = None,
    payment_types = None,
    action = None,
    cycle_number = None,
    cycle = None,
    hour = None,
    start_date = None,
    end_date = None,
    next_creation_date = None,
    email_sender = None,
    email_subject = None,
    email_message = None,
    email_filename = None,
    offer_id = None,
    confirmation_id = None
):
    """
    Creates the XML to add or edit a recurring
    """

    integer_field_names = [
        "client_id",
        "contact_id",
        "due_days",
        "discount_days",
        "cycle_number",
        "hour",
        "offer_id",
        "confirmation_id",
    ]
    date_or_string_fieldnames = [
        "supply_date"
    ]
    date_fieldnames = [
        "start_date",
        "end_date",
        "next_creation_date",
    ]
    float_fieldnames = [
        "quote"
    ]
    string_fieldnames = [
        "title",
        "address",
        "supply_date_type",
        "name",
        "label",
        "intro",
        "note",
        "currency_code",
        "reduction",
        "net_gross",
        "payment_types",
        "action",
        "cycle",
        "email_sender",
        "email_subject",
        "email_message",
        "email_filename",
    ]

    recurring_tag = ET.Element("recurring")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            recurring_tag.append(new_tag)

    # Date or string fields
    for field_name in date_or_string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            if isinstance(value, datetime.date):
                new_tag.text = value.isoformat()
            else:
                new_tag.text = unicode(value)
            recurring_tag.append(new_tag)

    # Date fields
    for field_name in date_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = value.isoformat()
            recurring_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            recurring_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            recurring_tag.append(new_tag)

    xml = ET.tostring(recurring_tag)

    # Finished
    return xml


class Recurring(Bunch):

    def __init__(self, conn, id = None, recurring_etree = None):
        """
        Recurring

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # integer
        self.created = None  # datetime
        self.client_id = None  # integer
        self.contact_id = None  # integer
        self.template_id = None  # integer
        self.currency_code = None
        self.name = None
        self.title = None
        self.cycle_number = None
        self.cycle = None  # DAILY, WEEKLY, MONTHLY, YEARLY
        self.action = None  # CREATE, COMPLETE, EMAIL
        self.hour = None  # integer
        self.start_date = None  # date
        self.end_date = None  # date
        self.last_creation_date = None  # date
        self.next_creation_date = None  # date
        self.iterations = None  # integer
        self.counter = None  # integer
        self.address = None  # Pass an empty value to use the current customer address.
        self.due_days = None  # integer
        self.discount_rate = None  # float
        self.discount_days = None  # integer
        self.intro = None
        self.note = None
        self.total_gross = None  # float
        self.total_net = None  # float
        self.net_gross = None  # NET, GROSS
        self.reduction = None
        self.total_gross_unreduced = None  # float
        self.total_net_unreduced = None  # float
        self.quote = None  # float
        self.ultimo = None  # integer
        self.label = None
        self.supply_date_type = None
        #     SUPPLY_DATE (Leistungsdatum als Datum)
        #     DELIVERY_DATE (Lieferdatum als Datum)
        #     SUPPLY_TEXT (Leistungsdatum als Freitext)
        #     DELIVERY_TEXT (Lieferdatum als Freitext)
        self.supply_date = None
        self.email_sender = None
        self.email_subject = None
        self.email_message = None
        self.email_filename = None
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
        self.offer_id = None
        self.confirmation_id = None

        if recurring_etree is not None:
            self.load_from_etree(recurring_etree)


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

            if text is not None:
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
        Loads the recurring-data from server
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # Path
        path = "/api/recurrings/{id}".format(id = self.id)

        # Fetch data
        response = self.conn.get(path = path)
        if not response.status == 200:
            raise errors.NotFoundError(unicode(self.id))

        # Fill in data from XML
        self.load_from_xml(response.data)
        self.content_language = response.headers.get("content-language", None)




    # @classmethod
    # def create(
    #     cls,
    #     conn,
    #     archived = None,
    #     number_pre = None,
    #     number = None,
    #     number_length = None,
    #     name = None,
    #     street = None,
    #     zip = None,
    #     city = None,
    #     state = None,
    #     country_code = None,
    #     first_name = None,
    #     last_name = None,
    #     salutation = None,
    #     phone = None,
    #     fax = None,
    #     mobile = None,
    #     email = None,
    #     www = None,
    #     tax_number = None,
    #     vat_number = None,
    #     bank_account_number = None,
    #     bank_account_owner = None,
    #     bank_number = None,
    #     bank_name = None,
    #     bank_swift = None,
    #     bank_iban = None,
    #     sepa_mandate = None,
    #     sepa_mandate_date = None,
    #     tax_rule = None,
    #     net_gross = None,
    #     default_payment_types = None,
    #     note = None,
    #     discount_rate_type = None,
    #     discount_rate = None,
    #     discount_days_type = None,
    #     discount_days = None,
    #     due_days_type = None,
    #     due_days = None,
    #     reminder_due_days_type = None,
    #     reminder_due_days = None,
    #     offer_validity_days_type = None,
    #     offer_validity_days = None,
    #     currency_code = None,
    #     price_group = None
    # ):
    #     """
    #     Creates one client
    #
    #     :param conn: Connection-Object
    #     :param archived: State of archival storage.
    #         True = archived, False = active
    #         Default value: False
    #     :param number_pre: Prefix
    #         Default value: Value from settings
    #     :param number: sequential number
    #         Default value: next free number
    #     :param number_length: Minimum length of the customer number
    #         (to be filled with leading zeros)
    #         Default value: Value from settings
    #     :param name: Company name
    #     :param street: Street
    #     :param zip: Zip code
    #     :param city: City
    #     :param state: State, county, district, region
    #     :param country_code: Country, Country code as ISO 3166 Alpha-2
    #         Default value: Value from your own company
    #     :param first_name: First name
    #     :param last_name: Last name
    #     :param salutation: Salutation
    #     :param phone: Phone
    #     :param fax: Fax
    #     :param mobile: Mobile number
    #     :param email: Email, valid Email address
    #     :param www: Website, URL (w/o http)
    #     :param tax_number: Tax number
    #     :param vat_number: VAT number, valid VAT number
    #     :param bank_account_number: Bank account number
    #     :param bank_account_owner: Bank account owner
    #     :param bank_number: Bank identifier code
    #     :param bank_name: Bank name
    #     :param bank_swift: SWIFT/BIC
    #     :param bank_iban: IBAN
    #     :param sepa_mandate: Mandate reference of a SEPA Direct Debit mandate
    #     :param sepa_mandate_date: Date of issue of the SEPA Direct Debit mandate
    #     :param tax_rule: Tax Rule
    #         Possible values: TAX, NO_TAX, COUNTRY
    #         Default value: "COUNTRY"
    #     :param default_payment_types: Payment Type(s)
    #         (eg. CASH, BANK_TRANSFER, PAYPAL, ...).
    #         More than one payment type could be given as a comma separated list.
    #         Theses payment types will be logically OR-connected.
    #         You can find a overview of all payment types at API documentation of
    #         payments. If no value is passed, the customer will be offered
    #         the payment types specified at the account settings.
    #     :param net_gross: Price basis (net, gross, according to account settings)
    #         Possible values: NET, GROSS, SETTINGS
    #         Default value: "SETTINGS"
    #     :param note: Note
    #     :param discount_rate_type: Type of the default value for discount rate
    #         Possible values: SETTINGS, ABSOLUTE, RELATIVE
    #         Default value: "SETTINGS"
    #     :param discount_rate: Discount rate
    #     :param discount_days_type: Type of the default value for discount interval
    #         Possible values: SETTINGS, ABSOLUTE, RELATIVE
    #         Default value: "SETTINGS"
    #     :param discount_days: Discount period in days
    #     :param due_days_type: Type of the default value for maturity
    #         Possible values: SETTINGS, ABSOLUTE, RELATIVE
    #         Default value: "SETTINGS"
    #     :param due_days: Maturity in days from invoice date
    #     :param reminder_due_days_type: Type of the default value for reminder
    #         maturity
    #         Possible values: SETTINGS, ABSOLUTE, RELATIVE
    #         Default value: "SETTINGS"
    #     :param reminder_due_days: Reminder maturity
    #     :param offer_validity_days_type: Type of the default value for
    #         validity of estimates
    #         Possible values: SETTINGS, ABSOLUTE, RELATIVE
    #         Default value: "SETTINGS"
    #     :param offer_validity_days: Validity of estimates
    #     :param currency_code: The currency for this client. ISO currency code.
    #         If this field is empty, the account currency is used.
    #     :param price_group: Artciles can have several prices.
    #         The pricegroup defines which price applies to the client.
    #     """
    #
    #     # XML
    #     xml = _client_xml(
    #         archived = archived,
    #         number_pre = number_pre,
    #         number = number,
    #         number_length = number_length,
    #         name = name,
    #         street = street,
    #         zip = zip,
    #         city = city,
    #         state = state,
    #         country_code = country_code,
    #         first_name = first_name,
    #         last_name = last_name,
    #         salutation = salutation,
    #         phone = phone,
    #         fax = fax,
    #         mobile = mobile,
    #         email = email,
    #         www = www,
    #         tax_number = tax_number,
    #         vat_number = vat_number,
    #         bank_account_number = bank_account_number,
    #         bank_account_owner = bank_account_owner,
    #         bank_number = bank_number,
    #         bank_name = bank_name,
    #         bank_swift = bank_swift,
    #         bank_iban = bank_iban,
    #         sepa_mandate = sepa_mandate,
    #         sepa_mandate_date = sepa_mandate_date,
    #         tax_rule = tax_rule,
    #         net_gross = net_gross,
    #         default_payment_types = default_payment_types,
    #         note = note,
    #         discount_rate_type = discount_rate_type,
    #         discount_rate = discount_rate,
    #         discount_days_type = discount_days_type,
    #         discount_days = discount_days,
    #         due_days_type = due_days_type,
    #         due_days = due_days,
    #         reminder_due_days_type = reminder_due_days_type,
    #         reminder_due_days = reminder_due_days,
    #         offer_validity_days_type = offer_validity_days_type,
    #         offer_validity_days = offer_validity_days,
    #         currency_code = currency_code,
    #         price_group = price_group
    #     )
    #
    #     # Path
    #     path = "/api/clients"
    #
    #     # Send POST-request
    #     response = conn.post(path = path, body = xml)
    #     if response.status != 201:  # Created
    #         raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))
    #
    #     # Create Client-Object
    #     client = cls(conn = conn)
    #     client.content_language = response.headers.get("content-language", None)
    #     client.load_from_xml(response.data)
    #
    #     # Finished
    #     return client






class Recurrings(list):

    def __init__(self, conn):
        """
        Recurrings-List

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
        name = None,
        payment_type = None,
        cycle = None,
        label = None,
        intro = None,
        note = None,
        tags = None,

        order_by = None,
        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with Recurring-objects

        If no search criteria given --> all recurrings will returned (REALLY ALL!).

        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param name: The Name of the recurring
        :param payment_type: Payment Type (eg. CASH, BANK_TRANSFER, PAYPAL, ...).
            More than one payment type could be given as a comma separated list.
            Theses payment types will be logically OR-connected.
            You can find a overview of all payment types at API documentation
            of payments.
        :param cycle: Interval (DAILY, WEEKLY, MONTHLY, YEARLY).
        :param label: Free text search in label text
        :param intro: Free text search in introductory text
        :param note: Free text search in explanatory notes
        :param tags: Comma seperated list of tags

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
                name,
                payment_type,
                cycle,
                label,
                intro,
                note,
                tags,
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
        url = Url(path = "/api/recurrings")
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
        if name:
            url.query["name"] = name
        if payment_type:
            url.query["payment_type"] = payment_type
        if cycle:
            url.query["cycle"] = cycle
        if label:
            url.query["label"] = label
        if intro:
            url.query["intro"] = intro
        if note:
            url.query["note"] = note
        if tags:
            url.query["tags"] = tags

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        recurrings_etree = ET.fromstring(response.data)

        self.per_page = int(recurrings_etree.attrib.get("per_page", "100"))
        self.total = int(recurrings_etree.attrib.get("total", "0"))
        self.page = int(recurrings_etree.attrib.get("page", "1"))
        self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))

        # Iterate over all recurrings
        for recurring_etree in recurrings_etree:
            self.append(Recurring(conn = self.conn, recurring_etree = recurring_etree))

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                client_id = client_id,
                contact_id = contact_id,
                name = name,
                payment_type = payment_type,
                cycle = cycle,
                label = label,
                intro = intro,
                note = note,
                tags = tags,

                order_by = order_by,
                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class RecurringsIterator(ItemsIterator):
    """
    Iterates over all found recurrings
    """

    def __init__(self, conn, per_page = 30):
        """
        RecurringsIterator
        """

        self.conn = conn
        self.items = Recurrings(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            client_id = None,
            contact_id = None,
            name = None,
            payment_type = None,
            cycle = None,
            label = None,
            intro = None,
            note = None,
            tags = None,
            order_by = None
        )


    def search(
        self,
        client_id = None,
        contact_id = None,
        name = None,
        payment_type = None,
        cycle = None,
        label = None,
        intro = None,
        note = None,
        tags = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.client_id = client_id
        self.search_params.contact_id = contact_id
        self.search_params.name = name
        self.search_params.payment_type = payment_type
        self.search_params.cycle = cycle
        self.search_params.label = label
        self.search_params.intro = intro
        self.search_params.note = note
        self.search_params.tags = tags
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            client_id = self.search_params.client_id,
            contact_id = self.search_params.contact_id,
            name = self.search_params.name,
            payment_type = self.search_params.payment_type,
            cycle = self.search_params.cycle,
            label = self.search_params.label,
            intro = self.search_params.intro,
            note = self.search_params.note,
            tags = self.search_params.tags,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )

