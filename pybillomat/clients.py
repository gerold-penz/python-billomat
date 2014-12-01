#!/usr/bin/env python
# coding: utf-8
"""
Clients

- English API-Description: http://www.billomat.com/en/api/clients
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/kunden
"""

import datetime
import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url


class Client(Bunch):

    def __init__(self, conn, id = None, client_etree = None):
        """
        Client

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # Integer
        self.created = None  # Datetime
        self.archived = None  # Boolean
        self.client_number = None
        self.number = None  # Integer
        self.number_pre = None
        self.name = None
        self.salutation = None
        self.first_name = None
        self.last_name = None
        self.street = None
        self.zip = None
        self.city = None
        self.state = None
        self.country_code = None
        self.phone = None
        self.fax = None
        self.mobile = None
        self.email = None
        self.www = None
        self.tax_number = None
        self.vat_number = None
        self.bank_account_owner = None
        self.bank_number = None
        self.bank_name = None
        self.bank_account_number = None
        self.bank_swift = None
        self.bank_iban = None
        self.sepa_mandate = None
        self.sepa_mandate_date = None
        self.tax_rule = None
        self.net_gross = None
        self.default_payment_types = None
        self.discount_rate_type = None
        self.discount_rate = None
        self.discount_days_type = None
        self.discount_days = None
        self.due_days_type = None
        self.due_days = None
        self.reminder_due_days_type = None
        self.reminder_due_days = None
        self.offer_validity_days_type = None
        self.offer_validity_days = None
        self.currency_code = None
        self.price_group = None
        self.note = None
        self.revenue_gross = None  # Float
        self.revenue_net = None  # Float"

        if client_etree is not None:
            self.load_from_etree(client_etree)


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
                elif type == "float":
                    setattr(self, tag, float(text))
                else:
                    if isinstance(text, str):
                        text = text.decode("utf-8")
                    setattr(self, tag, text)

            # <plan>L</plan>
            # <quotas>
                # <quota>
                    # <entity>documents</entity>
                    # <available>300</available>
                    # <used>22</used>
                # </quota>
                # <quota>
                    # <entity>clients</entity>
                    # <available>1500</available>
                    # <used>328</used>
                # </quota>
                # <quota>
                    # <entity>articles</entity>
                    # <available>5000</available>
                    # <used>16</used>
                # </quota>
                # <quota>
                    # <entity>storage</entity>
                    # <available>-1</available>
                    # <used>203782576</used>
                # </quota>
            # </quotas>


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
        Loads the client-data from server
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # Path
        path = "/api/clients/{id}".format(id = self.id)

        # Fetch data
        response = self.conn.get(path = path)
        if response.status != 200:
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Fill in data from XML
        self.load_from_xml(response.data)
        self.content_language = response.headers.get("content-language", None)


    @classmethod
    def create(
        cls,
        conn,
        archived = None,
        number_pre = None,
        number = None,
        number_length = None,
        name = None,
        street = None,
        zip = None,
        city = None,
        state = None,
        country_code = None,
        first_name = None,
        last_name = None,
        salutation = None,
        phone = None,
        fax = None,
        mobile = None,
        email = None,
        www = None,
        tax_number = None,
        vat_number = None,
        bank_account_number = None,
        bank_account_owner = None,
        bank_number = None,
        bank_name = None,
        bank_swift = None,
        bank_iban = None,
        sepa_mandate = None,
        sepa_mandate_date = None,
        tax_rule = None,
        net_gross = None,
        default_payment_types = None,
        note = None,
        discount_rate_type = None,
        discount_rate = None,
        discount_days_type = None,
        discount_days = None,
        due_days_type = None,
        due_days = None,
        reminder_due_days_type = None,
        reminder_due_days = None,
        offer_validity_days_type = None,
        offer_validity_days = None,
        currency_code = None,
        price_group = None
    ):
        """
        Creates one client

        :param conn: Connection-Object
        :param archived: State of archival storage.
            True = archived, False = active
            Default value: False
        :param number_pre: Prefix
            Default value: Value from settings
        :param number: sequential number
            Default value: next free number
        :param number_length: Minimum length of the customer number
            (to be filled with leading zeros)
            Default value: Value from settings
        :param name: Company name
        :param street: Street
        :param zip: Zip code
        :param city: City
        :param state: State, county, district, region
        :param country_code: Country, Country code as ISO 3166 Alpha-2
            Default value: Value from your own company
        :param first_name: First name
        :param last_name: Last name
        :param salutation: Salutation
        :param phone: Phone
        :param fax: Fax
        :param mobile: Mobile number
        :param email: Email, valid Email address
        :param www: Website, URL (w/o http)
        :param tax_number: Tax number
        :param vat_number: VAT number, valid VAT number
        :param bank_account_number: Bank account number
        :param bank_account_owner: Bank account owner
        :param bank_number: Bank identifier code
        :param bank_name: Bank name
        :param bank_swift: SWIFT/BIC
        :param bank_iban: IBAN
        :param sepa_mandate: Mandate reference of a SEPA Direct Debit mandate
        :param sepa_mandate_date: Date of issue of the SEPA Direct Debit mandate
        :param tax_rule: Tax Rule
            Possible values: TAX, NO_TAX, COUNTRY
            Default value: "COUNTRY"
        :param default_payment_types: Payment Type(s)
            (eg. CASH, BANK_TRANSFER, PAYPAL, ...).
            More than one payment type could be given as a comma separated list.
            Theses payment types will be logically OR-connected.
            You can find a overview of all payment types at API documentation of
            payments. If no value is passed, the customer will be offered
            the payment types specified at the account settings.
        :param net_gross: Price basis (net, gross, according to account settings)
            Possible values: NET, GROSS, SETTINGS
            Default value: "SETTINGS"
        :param note: Note
        :param discount_rate_type: Type of the default value for discount rate
            Possible values: SETTINGS, ABSOLUTE, RELATIVE
            Default value: "SETTINGS"
        :param discount_rate: Discount rate
        :param discount_days_type: Type of the default value for discount interval
            Possible values: SETTINGS, ABSOLUTE, RELATIVE
            Default value: "SETTINGS"
        :param discount_days: Discount period in days
        :param due_days_type: Type of the default value for maturity
            Possible values: SETTINGS, ABSOLUTE, RELATIVE
            Default value: "SETTINGS"
        :param due_days: Maturity in days from invoice date
        :param reminder_due_days_type: Type of the default value for reminder
            maturity
            Possible values: SETTINGS, ABSOLUTE, RELATIVE
            Default value: "SETTINGS"
        :param reminder_due_days: Reminder maturity
        :param offer_validity_days_type: Type of the default value for
            validity of estimates
            Possible values: SETTINGS, ABSOLUTE, RELATIVE
            Default value: "SETTINGS"
        :param offer_validity_days: Validity of estimates
        :param currency_code: The currency for this client. ISO currency code.
            If this field is empty, the account currency is used.
        :param price_group: Artciles can have several prices.
            The pricegroup defines which price applies to the client.
        """

        # XML
        client_tag = ET.Element("client")
        if not archived is None:
            archived_tag = ET.Element("archived")
            archived_tag.text = "1" if archived else "0"
            client_tag.append(archived_tag)
        if not number_pre is None:
            number_pre_tag = ET.Element("number_pre")
            number_pre_tag.text = unicode(number_pre)
            client_tag.append(number_pre_tag)
        if not number is None:
            number_tag = ET.Element("number")
            number_tag.text = unicode(int(number))
            client_tag.append(number_tag)
        if not number_length is None:
            number_length_tag = ET.Element("number_length")
            number_length_tag.text = unicode(int(number_length))
            client_tag.append(number_length_tag)
        if not name is None:
            name_tag = ET.Element("name")
            name_tag.text = unicode(name)
            client_tag.append(name_tag)
        if not street is None:
            street_tag = ET.Element("street")
            street_tag.text = unicode(street)
            client_tag.append(street_tag)
        if not zip is None:
            zip_tag = ET.Element("zip")
            zip_tag.text = unicode(zip)
            client_tag.append(zip_tag)
        if not city is None:
            city_tag = ET.Element("city")
            city_tag.text = unicode(city)
            client_tag.append(city_tag)
        if not state is None:
            state_tag = ET.Element("state")
            state_tag.text = unicode(state)
            client_tag.append(state_tag)
        if not country_code is None:
            country_code_tag = ET.Element("country_code")
            country_code_tag.text = unicode(country_code)
            client_tag.append(country_code_tag)
        if not first_name is None:
            first_name_tag = ET.Element("first_name")
            first_name_tag.text = unicode(first_name)
            client_tag.append(first_name_tag)
        if not last_name is None:
            last_name_tag = ET.Element("last_name")
            last_name_tag.text = unicode(last_name)
            client_tag.append(last_name_tag)
        if not salutation is None:
            salutation_tag = ET.Element("salutation")
            salutation_tag.text = unicode(salutation)
            client_tag.append(salutation_tag)
        if not phone is None:
            phone_tag = ET.Element("phone")
            phone_tag.text = unicode(phone)
            client_tag.append(phone_tag)
        if not fax is None:
            fax_tag = ET.Element("fax")
            fax_tag.text = unicode(fax)
            client_tag.append(fax_tag)
        if not mobile is None:
            mobile_tag = ET.Element("mobile")
            mobile_tag.text = unicode(mobile)
            client_tag.append(mobile_tag)
        if not email is None:
            email_tag = ET.Element("email")
            email_tag.text = unicode(email)
            client_tag.append(email_tag)
        if not www is None:
            www_tag = ET.Element("www")
            www_tag.text = unicode(www)
            client_tag.append(www_tag)
        if not tax_number is None:
            tax_number_tag = ET.Element("tax_number")
            tax_number_tag.text = unicode(tax_number)
            client_tag.append(tax_number_tag)
        if not vat_number is None:
            vat_number_tag = ET.Element("vat_number")
            vat_number_tag.text = unicode(vat_number)
            client_tag.append(vat_number_tag)
        if not bank_account_number is None:
            bank_account_number_tag = ET.Element("bank_account_number")
            bank_account_number_tag.text = unicode(bank_account_number)
            client_tag.append(bank_account_number_tag)
        if not bank_account_owner is None:
            bank_account_owner_tag = ET.Element("bank_account_owner")
            bank_account_owner_tag.text = unicode(bank_account_owner)
            client_tag.append(bank_account_owner_tag)
        if not bank_number is None:
            bank_number_tag = ET.Element("bank_number")
            bank_number_tag.text = unicode(bank_number)
            client_tag.append(bank_number_tag)
        if not bank_name is None:
            bank_name_tag = ET.Element("bank_name")
            bank_name_tag.text = unicode(bank_name)
            client_tag.append(bank_name_tag)
        if not bank_swift is None:
            bank_swift_tag = ET.Element("bank_swift")
            bank_swift_tag.text = unicode(bank_swift)
            client_tag.append(bank_swift_tag)
        if not bank_iban is None:
            bank_iban_tag = ET.Element("bank_iban")
            bank_iban_tag.text = unicode(bank_iban)
            client_tag.append(bank_iban_tag)
        if not sepa_mandate is None:
            sepa_mandate_tag = ET.Element("sepa_mandate")
            sepa_mandate_tag.text = unicode(sepa_mandate)
            client_tag.append(sepa_mandate_tag)
        if not sepa_mandate_date is None:
            assert isinstance(sepa_mandate_date, datetime.date)
            sepa_mandate_date_tag = ET.Element("sepa_mandate_date")
            sepa_mandate_date_tag.text = sepa_mandate_date.isoformat()
            client_tag.append(sepa_mandate_date_tag)
        if not tax_rule is None:
            assert unicode(tax_rule).upper() in ["TAX", "NO_TAX", "COUNTRY"] 
            tax_rule_tag = ET.Element("tax_rule")
            tax_rule_tag.text = unicode(tax_rule).upper()
            client_tag.append(tax_rule_tag)
        if not default_payment_types is None:
            if isinstance(default_payment_types, (list, tuple)):
                default_payment_types = ", ".join([
                    item.upper() for item in default_payment_types
                ])
            default_payment_types_tag = ET.Element("default_payment_types")
            default_payment_types_tag.text = unicode(default_payment_types)
            client_tag.append(default_payment_types_tag)
        if not net_gross is None:
            assert unicode(net_gross).upper() in ["NET", "GROSS", "SETTINGS"]
            net_gross_tag = ET.Element("net_gross")
            net_gross_tag.text = unicode(net_gross).upper()
            client_tag.append(net_gross_tag)
        if not note is None:
            note_tag = ET.Element("note")
            note_tag.text = unicode(note)
            client_tag.append(note_tag)
        if not discount_rate_type is None:
            assert unicode(discount_rate_type).upper() in [
                "ABSOLUTE", "RELATIVE", "SETTINGS"
            ]
            discount_rate_type_tag = ET.Element("discount_rate_type")
            discount_rate_type_tag.text = unicode(discount_rate_type).upper()
            client_tag.append(discount_rate_type_tag)
        if not discount_rate is None:
            discount_rate_tag = ET.Element("discount_rate")
            discount_rate_tag.text = unicode(float(discount_rate))
            client_tag.append(discount_rate_tag)
        if not discount_days_type is None:
            assert unicode(discount_days_type).upper() in [
                "ABSOLUTE", "RELATIVE", "SETTINGS"
            ]
            discount_days_type_tag = ET.Element("discount_days_type")
            discount_days_type_tag.text = unicode(discount_days_type).upper()
            client_tag.append(discount_days_type_tag)
        if not discount_days is None:
            discount_days_tag = ET.Element("discount_days")
            discount_days_tag.text = unicode(float(discount_days))
            client_tag.append(discount_days_tag)
        if not due_days_type is None:
            assert unicode(due_days_type).upper() in [
                "ABSOLUTE", "RELATIVE", "SETTINGS"
            ]
            due_days_type_tag = ET.Element("due_days_type")
            due_days_type_tag.text = unicode(due_days_type).upper()
            client_tag.append(due_days_type_tag)
        if not due_days is None:
            due_days_tag = ET.Element("due_days")
            due_days_tag.text = int(due_days)
            client_tag.append(due_days_tag)
        if not reminder_due_days_type is None:
            assert unicode(reminder_due_days_type).upper() in [
                "ABSOLUTE", "RELATIVE", "SETTINGS"
            ]
            reminder_due_days_type_tag = ET.Element("reminder_due_days_type")
            reminder_due_days_type_tag.text = unicode(reminder_due_days_type).upper()
            client_tag.append(reminder_due_days_type_tag)
        if not reminder_due_days is None:
            reminder_due_days_tag = ET.Element("reminder_due_days")
            reminder_due_days_tag.text = unicode(int(reminder_due_days))
            client_tag.append(reminder_due_days_tag)
        if not offer_validity_days_type is None:
            assert unicode(offer_validity_days_type).upper() in [
                "ABSOLUTE", "RELATIVE", "SETTINGS"
            ]
            offer_validity_days_type_tag = ET.Element("offer_validity_days_type")
            offer_validity_days_type_tag.text = unicode(offer_validity_days_type)
            client_tag.append(offer_validity_days_type_tag)
        if not offer_validity_days is None:
            offer_validity_days_tag = ET.Element("offer_validity_days")
            offer_validity_days_tag.text = unicode(int(offer_validity_days))
            client_tag.append(offer_validity_days_tag)
        if not currency_code is None:
            currency_code_tag = ET.Element("currency_code")
            currency_code_tag.text = unicode(currency_code)
            client_tag.append(currency_code_tag)
        if not price_group is None:
            price_group_tag = ET.Element("price_group")
            price_group_tag.text = unicode(int(price_group))
            client_tag.append(price_group_tag)

        xml = ET.tostring(client_tag)

        # Path
        path = "/api/clients"

        # Send POST-request
        response = conn.post(path = path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Client-Object
        client = cls(conn = conn)
        client.content_language = response.headers.get("content-language", None)
        client.load_from_xml(response.data)

        # Finished
        return client


    def delete(self, id = None):
        """
        Deletes one client
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # Path
        path = "/api/clients/{id}".format(id = self.id)

        # Fetch data
        response = self.conn.delete(path = path)
        if response.status != 200:
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))


class Clients(list):

    def __init__(self, conn):
        """
        Clients-List

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
        name = None,
        client_number = None,
        email = None,
        first_name = None,
        last_name = None,
        country_code = None,
        note = None,
        invoice_id = None,
        tags = None,
        order_by = None,

        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the (internal) list with Client-objects

        If no search criteria given --> all clients will returned (REALLY ALL!).

        :param name: Company name
        :param client_number: Client number
        :param email: E-mail address
        :param first_name: First name of the contact person
        :param last_name: Last name of the contact person
        :param country_code: Country code as ISO 3166 Alpha-2
        :param note: Note
        :param invoice_id: ID of an invoice of this client,
            multiple values seperated with comma
        :param tags: Comma seperated list of tags
        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        :param allow_empty_filter: If `True`, every filter-parameter may be empty.
            All clients will returned. !!! EVERY CLIENT !!!
        """
        
        # Check empty filter
        if not allow_empty_filter:
            if not any([
                name,
                client_number,
                email,
                first_name,
                last_name,
                country_code,
                note,
                invoice_id,
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
        url = Url(path = "/api/clients")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameters
        if name:
            url.query["name"] = name
        if client_number:
            url.query["client_number"] = client_number
        if email:
            url.query["email"] = email
        if first_name:
            url.query["first_name"] = first_name
        if last_name:
            url.query["last_name"] = last_name
        if country_code:
            url.query["country_code"] = country_code
        if note:
            url.query["note"] = note
        if invoice_id:
            url.query["invoice_id"] = invoice_id
        if tags:
            url.query["tags"] = tags

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        clients_etree = ET.fromstring(response.data)

        self.per_page = int(clients_etree.attrib.get("per_page", "0"))
        self.total = int(clients_etree.attrib.get("total", "0"))
        self.page = int(clients_etree.attrib.get("page", "1"))
        self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))

        # Iterate over all clients
        for client_etree in clients_etree:
            self.append(Client(conn = self.conn, client_etree = client_etree))

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                name = name,
                client_number = client_number,
                email = email,
                first_name = first_name,
                last_name = last_name,
                country_code = country_code,
                note = note,
                invoice_id = invoice_id,
                tags = tags,

                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class ClientsIterator(object):
    """
    Iterates over all found clients
    """

    def __init__(self, conn, per_page = 30):
        """
        ClientsIterator
        """

        self.conn = conn
        self.clients = Clients(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            name = None,
            client_number = None,
            email = None,
            first_name = None,
            last_name = None,
            country_code = None,
            note = None,
            invoice_id = None,
            tags = None,
            order_by = None,
        )


    def search(
        self,
        name = None,
        client_number = None,
        email = None,
        first_name = None,
        last_name = None,
        country_code = None,
        note = None,
        invoice_id = None,
        tags = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.name = name
        self.search_params.client_number = client_number
        self.search_params.email = email
        self.search_params.first_name = first_name
        self.search_params.last_name = last_name
        self.search_params.country_code = country_code
        self.search_params.note = note
        self.search_params.invoice_id = invoice_id
        self.search_params.tags = tags
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.clients.search(
            name = self.search_params.name,
            client_number = self.search_params.client_number,
            email = self.search_params.email,
            first_name = self.search_params.first_name,
            last_name = self.search_params.last_name,
            country_code = self.search_params.country_code,
            note = self.search_params.note,
            invoice_id = self.search_params.invoice_id,
            tags = self.search_params.tags,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


    def __len__(self):
        """
        Returns the count of found clients
        """

        return self.clients.total or 0


    def __iter__(self):
        """
        Iterate over all found items
        """

        if not self.clients.pages:
            return

        for page in range(1, self.clients.pages + 1):
            if not self.clients.page == page:
                self.load_page(page = page)
            for client in self.clients:
                yield client


    def __getitem__(self, key):
        """
        Returns the requested client from the pool of found clients
        """

        # List-Ids
        all_list_ids = range(len(self))
        requested_list_ids = all_list_ids[key]
        is_list = isinstance(requested_list_ids, list)
        if not is_list:
            requested_list_ids = [requested_list_ids]
        assert isinstance(requested_list_ids, list)

        result = []

        for list_id in requested_list_ids:

            # In welcher Seite befindet sich die gewünschte ID?
            for page_nr in range(1, self.clients.pages + 1):
                max_list_id = (page_nr * self.clients.per_page) - 1
                if list_id <= max_list_id:
                    page = page_nr
                    break
            else:
                raise AssertionError()

            # Load page if neccessary
            if not self.clients.page == page:
                self.load_page(page = page)

            # Add equested client-object to result
            list_id_in_page = list_id - ((page - 1) * self.clients.per_page)
            result.append(self.clients[list_id_in_page])

        if is_list:
            return result
        else:
            return result[0]



