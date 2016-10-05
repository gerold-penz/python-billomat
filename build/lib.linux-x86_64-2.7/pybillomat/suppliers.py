#!/usr/bin/env python
# coding: utf-8
"""
Suppliers

- English API-Description: http://www.billomat.com/en/api/suppliers
- Deutsche API-Beschreibung: http://www.billomat.com/api/lieferanten
"""


import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _supplier_xml(
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
    creditor_identifier = None,
    bank_account_number = None,
    bank_account_owner = None,
    bank_number = None,
    bank_name = None,
    bank_swift = None,
    bank_iban = None,
    note = None,
    client_number = None,
    currency_code = None
):
    """
    Creates the XML to add or edit a supplier
    """

    string_fieldnames = [
        "name",
        "street",
        "zip",
        "city",
        "state",
        "country_code",
        "first_name",
        "last_name",
        "salutation",
        "phone",
        "fax",
        "mobile",
        "email",
        "www",
        "tax_number",
        "vat_number",
        "creditor_identifier",
        "bank_account_number",
        "bank_account_owner",
        "bank_number",
        "bank_name",
        "bank_swift",
        "bank_iban",
        "note",
        "client_number",
        "currency_code"
    ]

    supplier_tag = ET.Element("supplier")

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            supplier_tag.append(new_tag)

    xml = ET.tostring(supplier_tag)

    # Finished
    return xml


class Supplier(Item):

    base_path = u"/api/suppliers"


    def __init__(self, conn, id = None, supplier_etree = None):
        """
        Supplier

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.created = None  # datetime
        self.name = None
        self.salutation = None
        self.first_name = None
        self.last_name = None
        self.street = None
        self.zip = None
        self.city = None
        self.state = None  # z.B. Bundesland
        self.country_code = None
        self.phone = None
        self.fax = None
        self.mobile = None
        self.email = None
        self.www = None
        self.tax_number = None
        self.vat_number = None
        self.creditor_identifier = None
        self.bank_account_owner = None
        self.bank_number = None
        self.bank_name = None
        self.bank_account_number = None
        self.bank_swift = None
        self.bank_iban = None
        self.currency_code = None
        self.note = None
        self.client_number = None
        self.costs_gross = None  # float
        self.costs_net = None

        if supplier_etree is not None:
            self.load_from_etree(supplier_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
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
        creditor_identifier = None,
        bank_account_number = None,
        bank_account_owner = None,
        bank_number = None,
        bank_name = None,
        bank_swift = None,
        bank_iban = None,
        note = None,
        client_number = None,
        currency_code = None
    ):
        """
        Creates a supplier

        :param conn: Connection-Object

        :param name: Company name
        :param street: Street
        :param zip: Zip code
        :param city: City
        :param state: State, country, district, region
        :param country_code: Land; Country code as ISO 3166 Alpha-2;
            Default: Value from your own company
        :param first_name: First name
        :param last_name: Last name
        :param salutation: Salutation
        :param phone: Phone
        :param fax: Fax
        :param mobile: Mobile number
        :param email: Email address
        :param www: Website
        :param tax_number: Tax number
        :param vat_number: VAT number
        :param creditor_identifier: SEPA creditor identifier
        :param bank_account_number: Bank account number
        :param bank_account_owner: Bank account owner
        :param bank_number: Bank identifier code
        :param bank_name: Bank name
        :param bank_swift: SWIFT/BIC
        :param bank_iban: IBAN
        :param note: Note
        :param client_number: Client number you may have at this supplier.
        :param currency_code: The currency for this client.
            If this field is empty, the account currency is used.
        """

        # XML
        xml = _supplier_xml(
            name = name,
            street = street,
            zip = zip,
            city = city,
            state = state,
            country_code = country_code,
            first_name = first_name,
            last_name = last_name,
            salutation = salutation,
            phone = phone,
            fax = fax,
            mobile = mobile,
            email = email,
            www = www,
            tax_number = tax_number,
            vat_number = vat_number,
            creditor_identifier = creditor_identifier,
            bank_account_number = bank_account_number,
            bank_account_owner = bank_account_owner,
            bank_number = bank_number,
            bank_name = bank_name,
            bank_swift = bank_swift,
            bank_iban = bank_iban,
            note = note,
            client_number = client_number,
            currency_code = currency_code
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Supplier-Object
        supplier = cls(conn = conn)
        supplier.content_language = response.headers.get("content-language", None)
        supplier.load_from_xml(response.data)

        # Finished
        return supplier


    def edit(
        self,
        id = None,
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
        creditor_identifier = None,
        bank_account_number = None,
        bank_account_owner = None,
        bank_number = None,
        bank_name = None,
        bank_swift = None,
        bank_iban = None,
        note = None,
        client_number = None,
        currency_code = None
    ):
        """
        Edit a supplier-item

        :param id: ID of the supplier-item

        :param name: Company name
        :param street: Street
        :param zip: Zip code
        :param city: City
        :param state: State, country, district, region
        :param country_code: Land; Country code as ISO 3166 Alpha-2;
            Default: Value from your own company
        :param first_name: First name
        :param last_name: Last name
        :param salutation: Salutation
        :param phone: Phone
        :param fax: Fax
        :param mobile: Mobile number
        :param email: Email address
        :param www: Website
        :param tax_number: Tax number
        :param vat_number: VAT number
        :param creditor_identifier: SEPA creditor identifier
        :param bank_account_number: Bank account number
        :param bank_account_owner: Bank account owner
        :param bank_number: Bank identifier code
        :param bank_name: Bank name
        :param bank_swift: SWIFT/BIC
        :param bank_iban: IBAN
        :param note: Note
        :param client_number: Client number you may have at this supplier.
        :param currency_code: The currency for this client.
            If this field is empty, the account currency is used.

        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _supplier_xml(
            name = name,
            street = street,
            zip = zip,
            city = city,
            state = state,
            country_code = country_code,
            first_name = first_name,
            last_name = last_name,
            salutation = salutation,
            phone = phone,
            fax = fax,
            mobile = mobile,
            email = email,
            www = www,
            tax_number = tax_number,
            vat_number = vat_number,
            creditor_identifier = creditor_identifier,
            bank_account_number = bank_account_number,
            bank_account_owner = bank_account_owner,
            bank_number = bank_number,
            bank_name = bank_name,
            bank_swift = bank_swift,
            bank_iban = bank_iban,
            note = note,
            client_number = client_number,
            currency_code = currency_code
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


class Suppliers(list):

    def __init__(self, conn):
        """
        Suppliers-List

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
        email = None,
        first_name = None,
        last_name = None,
        country_code = None,
        creditor_identifier = None,
        note = None,
        client_number = None,
        incoming_id = None,
        tags = None,

        order_by = None,
        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with Supplier-objects

        :param name: Company name
        :param email: E-mail address
        :param first_name: First name of the contact person
        :param last_name: Last name of the contact person
        :param country_code: Country code as ISO 3166 Alpha-2
        :param creditor_identifier: SEPA creditor identifier
        :param note: Note
        :param client_number: Client number you may have at this supplier.
        :param incoming_id: ID of an incoming of this supplier,
            multiple values seperated with commas
        :param tags: Comma seperated list of tags.

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
                name,
                email,
                first_name,
                last_name,
                country_code,
                creditor_identifier,
                note,
                client_number,
                incoming_id,
                tags
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
        url = Url(path = "/api/suppliers")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameter
        if name is not None:
            url.query["name"] = name
        if email is not None:
            url.query["email"] = email
        if first_name is not None:
            url.query["first_name"] = first_name
        if last_name is not None:
            url.query["last_name"] = last_name
        if country_code is not None:
            url.query["country_code"] = country_code
        if creditor_identifier is not None:
            url.query["creditor_identifier"] = creditor_identifier
        if note is not None:
            url.query["note"] = note
        if client_number is not None:
            url.query["client_number"] = client_number
        if incoming_id is not None:
            url.query["incoming_id"] = incoming_id
        if tags is not None:
            url.query["tags"] = tags

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        suppliers_etree = ET.fromstring(response.data)

        self.per_page = int(suppliers_etree.attrib.get("per_page", "100"))
        self.total = int(suppliers_etree.attrib.get("total", "0"))
        self.page = int(suppliers_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all suppliers
        for supplier_etree in suppliers_etree:
            self.append(
                Supplier(conn = self.conn, supplier_etree = supplier_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                name = name,
                email = email,
                first_name = first_name,
                last_name = last_name,
                country_code = country_code,
                creditor_identifier = creditor_identifier,
                note = note,
                client_number = client_number,
                incoming_id = incoming_id,
                tags = tags,

                order_by = order_by,
                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class SuppliersIterator(ItemsIterator):
    """
    Iterates over all found suppliers
    """

    def __init__(self, conn, per_page = 30):
        """
        SuppliersIterator
        """

        self.conn = conn
        self.items = Suppliers(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            name = None,
            email = None,
            first_name = None,
            last_name = None,
            country_code = None,
            creditor_identifier = None,
            note = None,
            client_number = None,
            incoming_id = None,
            tags = None,
            order_by = None
        )


    def search(
        self,

        name = None,
        email = None,
        first_name = None,
        last_name = None,
        country_code = None,
        creditor_identifier = None,
        note = None,
        client_number = None,
        incoming_id = None,
        tags = None,

        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.name = name
        self.search_params.email = email
        self.search_params.first_name = first_name
        self.search_params.last_name = last_name
        self.search_params.country_code = country_code
        self.search_params.creditor_identifier = creditor_identifier
        self.search_params.note = note
        self.search_params.client_number = client_number
        self.search_params.incoming_id = incoming_id
        self.search_params.tags = tags

        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(

            name = self.search_params.name,
            email = self.search_params.email,
            first_name = self.search_params.first_name,
            last_name = self.search_params.last_name,
            country_code = self.search_params.country_code,
            creditor_identifier = self.search_params.creditor_identifier,
            note = self.search_params.note,
            client_number = self.search_params.client_number,
            incoming_id = self.search_params.incoming_id,
            tags = self.search_params.tags,

            order_by = self.search_params.order_by,
            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


