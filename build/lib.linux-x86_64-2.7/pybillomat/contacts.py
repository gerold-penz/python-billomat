#!/usr/bin/env python
# coding: utf-8
"""
Contacts

- English API-Description: http://www.billomat.com/en/api/clients/contacts
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/kunden/kontakte
"""


import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _contact_xml(
    client_id = None,
    label = None,
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
    www = None
):
    """
    Creates the XML to add or edit a contact
    """

    integer_fieldnames = [
        "client_id",
    ]
    string_fieldnames = [
        "label",
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
    ]

    contact_tag = ET.Element("contact")

    # Integer Fields
    for field_name in integer_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            contact_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            contact_tag.append(new_tag)

    xml = ET.tostring(contact_tag)

    # Finished
    return xml


class Contact(Item):

    base_path = u"/api/contacts"


    def __init__(self, conn, id = None, contact_etree = None):
        """
        Contact

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.created = None  # datetime
        self.client_id = None  # integer
        self.label = None
        self.name = None
        self.street = None
        self.zip = None
        self.city = None
        self.state = None
        self.country_code = None
        self.first_name = None
        self.last_name = None
        self.salutation = None
        self.phone = None
        self.fax = None
        self.mobile = None
        self.email = None
        self.www = None

        if contact_etree is not None:
            self.load_from_etree(contact_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        client_id = None,
        label = None,
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
        www = None
    ):
        """
        Creates a contact

        :param conn: Connection-Object

        :param client_id: ID of the client
        :param label: Label
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
        :param mobile: Mobile Number
        :param email: Email
        :param www: Website
        """

        # XML
        xml = _contact_xml(
            client_id = client_id,
            label = label,
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
            www = www
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Contact-Object
        contact = cls(conn = conn)
        contact.content_language = response.headers.get("content-language", None)
        contact.load_from_xml(response.data)

        # Finished
        return contact


    def edit(
        self,
        id = None,
        client_id = None,
        label = None,
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
        www = None
    ):
        """
        Edit a contact-item

        :param id: ID of the contact-item

        :param client_id: ID of the client
        :param label: Label
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
        :param mobile: Mobile Number
        :param email: Email
        :param www: Website
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _contact_xml(
            client_id = client_id,
            label = label,
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
            www = www
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


class Contacts(list):

    def __init__(self, conn):
        """
        Conntacts-List

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

        order_by = None,
        fetch_all = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with Contact-objects

        :param client_id: ID of the client (mandatory)

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        """

        # Check empty param
        if not client_id:
            raise errors.EmptyFilterError()

        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Url and system-parameters
        url = Url(path = "/api/contacts")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameter
        url.query["client_id"] = client_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        contacts_etree = ET.fromstring(response.data)

        self.per_page = int(contacts_etree.attrib.get("per_page", "100"))
        self.total = int(contacts_etree.attrib.get("total", "0"))
        self.page = int(contacts_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all contacts
        for contact_etree in contacts_etree:
            self.append(
                Contact(conn = self.conn, contact_etree = contact_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                client_id = client_id,

                order_by = order_by,
                fetch_all = fetch_all,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class ContactsIterator(ItemsIterator):
    """
    Iterates over all found contacts
    """

    def __init__(self, conn, per_page = 30):
        """
        ContactsIterator
        """

        self.conn = conn
        self.items = Contacts(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            client_id = None,
            order_by = None
        )


    def search(
        self,
        client_id = None,

        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.client_id = client_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            client_id = self.search_params.client_id,

            order_by = self.search_params.order_by,
            fetch_all = False,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


