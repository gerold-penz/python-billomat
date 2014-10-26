#!/usr/bin/env python
# coding: utf-8
"""
Clients

- English API-Description: http://www.billomat.com/en/api/clients
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/kunden
"""

import datetime
import xml.etree.ElementTree as etree
from bunch import Bunch


class Client(Bunch):

    def __init__(self, conn):
        """
        Client

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

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

        self.conn = conn


    @classmethod
    def from_etree(cls, conn, etree_element):
        """
        Returns Client-object from ElementTree-Element
        """

        client = cls(conn = conn)

        for item in etree_element:

            # Get data
            isinstance(item, etree.Element)
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
        root = etree.fromstring(xml_string)

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


class Clients(object):


    def __init__(self, conn):
        """
        Clients

        :param conn: Connection-Object
        """

        self.conn = conn


    @classmethod
    def from_search(
        cls,
        conn,
        name = None,
        client_number = None,
        email = None,
        first_name = None,
        last_name = None,
        country_code = None,
        note = None,
        invoice_id = None,
        tags = None
    ):
        """
        Returns Client-object

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
        """

        # Path
        path = "/api/clients"

        # Suchparameter
        if name:
            path += "?name={name}".format(name = name)
        # ...




        # # Request
        # request = conn.request(method = "GET", url = path)
        #
        # # Create new client-object from XML
        # client = cls.from_xml(conn, request.data)
        # client.content_language = request.headers.get("content-language", None)
        #
        # # Finished
        # return client

