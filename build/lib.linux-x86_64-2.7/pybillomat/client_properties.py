#!/usr/bin/env python
# coding: utf-8
"""
Client-Properties

- English API-Description: http://www.billomat.com/en/api/clients/properties
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/kunden/attribute
"""

import urllib3
import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


class ClientProperty(Item):

    base_path = u"/api/client-property-values"


    def __init__(self, conn, id = None, property_etree = None):
        """
        ClientPropertyValue

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # Integer
        self.client_id = None  # Integer
        self.client_property_id = None  # Integer
        self.type = None  # TEXTFIELD, CHECKBOX, TEXTAREA, ...
        self.name = None
        self.value = None

        if property_etree is not None:
            self.load_from_etree(property_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        client_id,
        client_property_id,
        value
    ):
        """
        Creates one Property

        :param conn: Connection-Object
        :param client_id: ID of the client
        :param client_property_id: ID of the property
        :param value: Property value
        """

        # XML
        property_tag = ET.Element("client-property-value")

        client_id_tag = ET.Element("client_id")
        client_id_tag.text = unicode(int(client_id))
        property_tag.append(client_id_tag)

        client_property_id_tag = ET.Element("client_property_id")
        client_property_id_tag.text = unicode(int(client_property_id))
        property_tag.append(client_property_id_tag)

        value_tag = ET.Element("value")
        value_tag.text = unicode(value)
        property_tag.append(value_tag)

        xml = ET.tostring(property_tag)

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Property-Object
        property = cls(conn = conn)
        property.load_from_xml(response.data)

        # Finished
        return property


class ClientProperties(list):

    def __init__(self, conn):
        """
        ClientProperty-List

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
        client_property_id = None,
        value = None,
        order_by = None,

        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the (internal) list with ClientPropertyValue-objects

        If no search criteria given --> all properties will returned (REALLY ALL!).

        :param client_id: Client ID
        :param client_property_id: Client-Property-ID
        :param value: Value of the Client-Property
        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        :param allow_empty_filter: If `True`, every filter-parameter may be empty.
            All client-properties will returned. !!! EVERY !!!
        """

        # Check empty filter
        if not allow_empty_filter:
            if not any([
                client_id,
                client_property_id,
                value
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
        url = Url(path = "/api/client-property-values")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameters
        if client_id:
            url.query["client_id"] = client_id
        if client_property_id:
            url.query["client_property_id"] = client_property_id
        if value is not None:
            url.query["value"] = value

        # Fetch data
        response = self.conn.get(path = str(url))
        if response.status != 200:
            # Check if "Unothorized" --> raise NoClientFoundError
            errors_etree = ET.fromstring(response.data)
            for error_etree in errors_etree:
                text = error_etree.text
                if text.lower() == "unauthorized":
                    raise errors.NotFoundError(
                        u"client_id: {client_id}".format(client_id = client_id)
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
        properties_etree = ET.fromstring(response.data)

        self.per_page = int(properties_etree.attrib.get("per_page", "0"))
        self.total = int(properties_etree.attrib.get("total", "0"))
        self.page = int(properties_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all client-properties
        for property_etree in properties_etree:
            self.append(
                ClientProperty(conn = self.conn, property_etree = property_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                client_id = client_id,
                client_property_id = client_property_id,
                value = value,

                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class ClientPropertiesIterator(ItemsIterator):
    """
    Iterates over all found properties
    """

    def __init__(self, conn, per_page = 100):
        """
        ClientPropertiesIterator
        """

        self.conn = conn
        self.items = ClientProperties(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            client_id = None,
            client_property_id = None,
            value = None,
            order_by = None,
        )


    def search(
        self,
        client_id = None,
        client_property_id = None,
        value = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.client_id = client_id
        self.search_params.client_property_id = client_property_id
        self.search_params.value = value
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            client_id = self.search_params.client_id,
            client_property_id = self.search_params.client_property_id,
            value = self.search_params.value,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


