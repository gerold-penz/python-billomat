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


class ClientProperty(Bunch):

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

        if not property_etree is None:
            self.load_from_etree(property_etree)


    def load_from_etree(self, etree_element):
        """
        Loads data from Element-Tree
        """

        for item in etree_element:

            # Get data
            isinstance(item, ET.Element)
            tag = item.tag
            tag_type = item.attrib.get("type")
            text = item.text

            if not text is None:
                if tag_type == "integer":
                    setattr(self, tag, int(text))
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
        Loads the property-data from server
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # Path
        path = "/api/client-property-values/{id}".format(id = self.id)

        # Fetch data
        response = self.conn.get(path = path)
        if response.status != 200:
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Fill in data from XML
        self.load_from_xml(response.data)


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
                client_id,
                client_property_id,
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

        # Fetch data
        response = self.conn.get(path = str(url))
        if response.status != 200:
            # Check if "Unothorized" --> raise NoClientFoundError
            errors_etree = ET.fromstring(response.data)
            for error_etree in errors_etree:
                text = error_etree.text
                if text.lower() == "unauthorized":
                    raise errors.ClientNotFoundError(
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
        self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))

        # Iterate over all clients
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

                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class ClientPropertiesIterator(object):
    """
    Iterates over all found properties
    """

    def __init__(self, conn, per_page = 100):
        """
        ClientPropertiesIterator
        """

        self.conn = conn
        self.client_properties = ClientProperties(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            client_id = None,
            client_property_id = None,
            order_by = None,
        )


    def search(
        self,
        client_id = None,
        client_property_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.client_id = client_id
        self.search_params.client_property_id = client_property_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.client_properties.search(
            client_id = self.search_params.client_id,
            client_property_id = self.search_params.client_property_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


    def __len__(self):
        """
        Returns the count of found properties
        """

        return self.client_properties.total or 0


    def __iter__(self):
        """
        Iterate over all found items
        """

        if not self.client_properties.pages:
            return

        for page in range(1, self.client_properties.pages + 1):
            if not self.client_properties.page == page:
                self.load_page(page = page)
            for client in self.client_properties:
                yield client


    def __getitem__(self, key):
        """
        Returns the requested property from the pool of found properties
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
            for page_nr in range(1, self.client_properties.pages + 1):
                max_list_id = (page_nr * self.client_properties.per_page) - 1
                if list_id <= max_list_id:
                    page = page_nr
                    break
            else:
                raise AssertionError()

            # Load page if neccessary
            if not self.client_properties.page == page:
                self.load_page(page = page)

            # Add equested client-object to result
            list_id_in_page = list_id - ((page - 1) * self.client_properties.per_page)
            result.append(self.client_properties[list_id_in_page])

        if is_list:
            return result
        else:
            return result[0]



