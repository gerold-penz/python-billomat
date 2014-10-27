#!/usr/bin/env python
# coding: utf-8
"""
Clients

- English API-Description: http://www.billomat.com/en/api/clients
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/kunden
"""

import datetime
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from errors import EmptyFilterError


class Client(Bunch):

    def __init__(self, conn):
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


    @classmethod
    def from_etree(cls, conn, etree_element):
        """
        Returns Client-object from ElementTree-Element
        """

        client = cls(conn = conn)

        for item in etree_element:

            # Get data
            isinstance(item, ET.Element)
            tag = item.tag
            type = item.attrib.get("type")
            text = item.text

            if not text is None:
                if type == "integer":
                    setattr(client, tag, int(text))
                elif type == "datetime":
                    # <created type="datetime">2011-10-04T17:40:00+02:00</created>
                    dt = datetime.datetime.strptime(text[:19], "%Y-%m-%dT%H:%M:%S")
                    setattr(client, tag, dt)
                elif type == "float":
                    setattr(client, tag, float(text))
                else:
                    if isinstance(text, str):
                        text = text.decode("utf-8")
                    setattr(client, tag, text)

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

        # Finished
        return client


    @classmethod
    def from_xml(cls, conn, xml_string):
        """
        Returns new Client-object from XML-string
        """

        # Parse XML
        root = ET.fromstring(xml_string)

        # Finished
        return cls.from_etree(conn, root)


    @classmethod
    def get(cls, conn, id = None):
        """
        Returns Client-object
        """

        # Path
        path = "/api/clients/{id}".format(id = id)

        # Request
        request = conn.request(method = "GET", url = path)

        # Create new client-object from XML
        client = cls.from_xml(conn, request.data)
        client.content_language = request.headers.get("content-language", None)

        # Finished
        return client


class Clients(list):


    def __init__(self, conn):
        """
        Clients

        :param conn: Connection-Object
        """

        list.__init__(self)

        self.conn = conn
        self.per_page = None
        self.total = None
        self.page = None


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
        page = 1
    ):
        """
        Fills the list with Client-objects

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
            So, all clients will returned. !!! EVERY INVOICE !!!
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
                raise EmptyFilterError()
        
        # Empty the list
        if not keep_old_items:
            while True:
                try:
                    self.pop()
                except IndexError:
                    break

        # Search parameters
        url = Url(path = "/api/clients")
        url.query["page"] = page
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

        # Request
        request = self.conn.request(method = "GET", url = str(url))

        # Iterate over all clients
        clients_etree = ET.fromstring(request.data)

        self.per_page = int(clients_etree.attrib.get("per_page", "0"))
        self.total = int(clients_etree.attrib.get("total", "0"))
        self.page = int(clients_etree.attrib.get("page", "1"))

        for client_etree in clients_etree:
            self.append(Client.from_etree(self.conn, client_etree))

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
                page = page + 1
            )


