#!/usr/bin/env python
# coding: utf-8
"""
Clients-Properties

- English API-Description: http://www.billomat.com/en/api/clients/properties
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/kunden/attribute
"""

import datetime
import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url


class ClientsProperty(Bunch):

    def __init__(self, conn, id = None, property_etree = None):
        """
        ClientsProperty

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


class ClientsProperties(list):

    def __init__(self, conn):
        """
        ClientsProperties-List

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

        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the (internal) list with ClientsProperty-objects

        If no search criteria given --> all properties will returned (REALLY ALL!).

        :param client_id: Client ID
        :param client_property_id: Client-Property-ID

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

        # Search parameters
        if client_id:
            url.query["client_id"] = client_id
        if client_property_id:
            url.query["client_property_id"] = client_property_id

        # Fetch data
        response = self.conn.get(path = str(url))
        if response.status != 200:


            print
            print response.status
            print
            print response.data
            print


            # Check if "Unothorized"-Error
            errors_etree = ET.fromstring(response.data)
            for error_etree in errors_etree:
                text = error_etree.text
                if text.lower() == "unauthorized":
                    raise errors.ClientNotFoundError(
                        u"client_id: {client_id}".format(client_id = client_id)
                    )

            # Other Error
            raise errors.BillomatError(response.data)

        # Parse XML
        properties_etree = ET.fromstring(response.data)

        self.per_page = int(properties_etree.attrib.get("per_page", "0"))
        self.total = int(properties_etree.attrib.get("total", "0"))
        self.page = int(properties_etree.attrib.get("page", "1"))
        self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))

        # Iterate over all clients
        for property_etree in properties_etree:
            self.append(ClientsProperty(conn = self.conn, property_etree = property_etree))

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


# class ClientsIterator(object):
#     """
#     Iterates over all found clients
#     """
#
#     def __init__(self, conn, per_page = 30):
#         """
#         ClientsIterator
#         """
#
#         self.conn = conn
#         self.clients = Clients(self.conn)
#         self.per_page = per_page
#         self.search_params = Bunch(
#             name = None,
#             client_number = None,
#             email = None,
#             first_name = None,
#             last_name = None,
#             country_code = None,
#             note = None,
#             invoice_id = None,
#             tags = None,
#         )
#
#
#     def search(
#         self,
#         name = None,
#         client_number = None,
#         email = None,
#         first_name = None,
#         last_name = None,
#         country_code = None,
#         note = None,
#         invoice_id = None,
#         tags = None,
#     ):
#         """
#         Search
#         """
#
#         # Params
#         self.search_params.name = name
#         self.search_params.client_number = client_number
#         self.search_params.email = email
#         self.search_params.first_name = first_name
#         self.search_params.last_name = last_name
#         self.search_params.country_code = country_code
#         self.search_params.note = note
#         self.search_params.invoice_id = invoice_id
#         self.search_params.tags = tags
#
#         # Search and prepare first page as result
#         self.load_page(1)
#
#
#     def load_page(self, page):
#
#         self.clients.search(
#             name = self.search_params.name,
#             client_number = self.search_params.client_number,
#             email = self.search_params.email,
#             first_name = self.search_params.first_name,
#             last_name = self.search_params.last_name,
#             country_code = self.search_params.country_code,
#             note = self.search_params.note,
#             invoice_id = self.search_params.invoice_id,
#             tags = self.search_params.tags,
#             fetch_all = False,
#             allow_empty_filter = True,
#             keep_old_items = False,
#             page = page,
#             per_page = self.per_page
#         )
#
#
#     def __len__(self):
#         """
#         Returns the count of found clients
#         """
#
#         return self.clients.total or 0
#
#
#     def __iter__(self):
#         """
#         Iterate over all found items
#         """
#
#         for page in range(1, self.clients.pages + 1):
#             if not self.clients.page == page:
#                 self.load_page(page = page)
#             for client in self.clients:
#                 yield client
#
#
#     def __getitem__(self, key):
#         """
#         Returns the requested client from the pool of found clients
#         """
#
#         # List-Ids
#         all_list_ids = range(len(self))
#         requested_list_ids = all_list_ids[key]
#         is_list = isinstance(requested_list_ids, list)
#         if not is_list:
#             requested_list_ids = [requested_list_ids]
#
#         result = []
#
#         for list_id in requested_list_ids:
#
#             # In welcher Seite befindet sich die gewünschte ID?
#             for page_nr in range(1, self.clients.pages + 1):
#                 max_list_id = (page_nr * self.clients.per_page) - 1
#                 if list_id <= max_list_id:
#                     page = page_nr
#                     break
#             else:
#                 raise AssertionError()
#
#             # Load page if neccessary
#             if not self.clients.page == page:
#                 self.load_page(page = page)
#
#             # Add equested client-object to result
#             list_id_in_page = list_id - ((page - 1) * self.clients.per_page)
#             result.append(self.clients[list_id_in_page])
#
#         if is_list:
#             return result
#         else:
#             return result[0]
#
#
#
