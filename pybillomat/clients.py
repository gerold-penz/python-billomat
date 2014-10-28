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

        self.id = None  # Integer
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

        if not client_etree is None:
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
        path = "/api/clients/{id}".format(id = id)

        # Fetch data
        response = self.conn.get(path = path)
        if not response.status == 200:
            raise errors.ClientNotFoundError(unicode(self.id))

        # Fill in data from XML
        self.load_from_xml(response.data)
        self.content_language = response.headers.get("content-language", None)


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



