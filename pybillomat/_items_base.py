#!/usr/bin/env python
# coding: utf-8

import datetime
import errors
import xml.etree.ElementTree as ET
from bunch import Bunch


class Item(Bunch):
    """
    Item

    Base class for Client, Recurring, ...
    """

    id = None
    content_language = None
    base_path = u"/api/<object>"


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
        path = "{base_path}/{id}".format(
            base_path = self.base_path,
            id = self.id
        )

        # Fetch data
        response = self.conn.get(path = path)
        if response.status != 200:
            # Check if "Unothorized" --> raise NotFoundError
            errors_etree = ET.fromstring(response.data)
            for error_etree in errors_etree:
                text = error_etree.text
                if (
                    text.lower() == "unauthorized" or
                    text.lower() == "row not found"
                ):
                    raise errors.NotFoundError(
                        u"id: {id}".format(id = self.id)
                    )
            # Other Error
            raise errors.BillomatError(response.data)

        # Fill in data from XML
        self.load_from_xml(response.data)
        self.content_language = response.headers.get("content-language", None)


    def delete(self, id = None):
        """
        Deletes an item
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # Path
        path = "{base_path}/{id}".format(
            base_path = self.base_path,
            id = self.id
        )

        # Fetch data
        response = self.conn.delete(path = path)
        if response.status != 200:
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))


class ItemsIterator(object):
    """
    ItemsIterator

    Base class for ClientsIterator, RecurringsIterator, ...
    """

    items = None


    def search(self):
        raise NotImplementedError()


    def load_page(self, page):
        raise NotImplementedError()


    def __len__(self):
        """
        Returns the count of found recurrings
        """

        return self.items.total or 0


    def __iter__(self):
        """
        Iterate over all found items
        """

        if not self.items.pages:
            return

        for page in range(1, self.items.pages + 1):
            if not self.items.page == page:
                self.load_page(page = page)
            for item in self.items:
                yield item


    def __getitem__(self, key):
        """
        Returns the requested item from the pool of found items
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
            for page_nr in range(1, self.items.pages + 1):
                max_list_id = (page_nr * self.items.per_page) - 1
                if list_id <= max_list_id:
                    page = page_nr
                    break
            else:
                raise AssertionError()

            # Load page if neccessary
            if not self.items.page == page:
                self.load_page(page = page)

            # Add equested invoice-object to result
            list_id_in_page = list_id - ((page - 1) * self.items.per_page)
            result.append(self.items[list_id_in_page])

        if is_list:
            return result
        else:
            return result[0]




