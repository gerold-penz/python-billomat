#!/usr/bin/env python
# coding: utf-8
"""
Recurring-Tags

- English API-Description: http://www.billomat.com/en/api/recurrings/tags
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/abo-rechnungen/schlagworte
"""

import urllib3
import xml.etree.ElementTree as ET
import errors
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


class RecurringTag(Item):

    base_path = u"/api/recurring-tags"


    def __init__(self, conn, id = None, tag_etree = None):
        """
        RecurringTag

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # Integer
        self.recurring_id = None  # Not always filled
        self.name = None
        self.count = None  # Not always filled

        if tag_etree is not None:
            self.load_from_etree(tag_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        recurring_id,
        name
    ):
        """
        Creates one recurring-tag

        :param conn: Connection-Object
        :param recurring_id: ID of the recurring
        :param name: Name of the tag
        """

        # XML
        recurring_tag = ET.Element("recurring-tag")

        recurring_id_tag = ET.Element("recurring_id")
        recurring_id_tag.text = unicode(int(recurring_id))
        recurring_tag.append(recurring_id_tag)

        name_tag = ET.Element("name")
        name_tag.text = unicode(name)
        recurring_tag.append(name_tag)

        xml = ET.tostring(recurring_tag)

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Item-Object from XML
        item_object = cls(conn = conn)
        item_object.load_from_xml(response.data)

        # Finished
        return item_object


class RecurringTags(list):

    def __init__(self, conn):
        """
        RecurringTags-List

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
        recurring_id = None,
        order_by = None,

        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the (internal) list with RecurringTag-objects

        If no search criteria given --> all tags will returned (REALLY ALL!).

        :param recurring_id: Recurring ID
        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        :param allow_empty_filter: If `True`, every filter-parameter may be empty.
            All recurring-tags will returned. !!! EVERY !!!
        """

        # Check empty filter
        if not allow_empty_filter:
            if not any([
                recurring_id,
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
        url = Url(path = "/api/recurring-tags")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameters
        if recurring_id:
            url.query["recurring_id"] = recurring_id

        # Fetch data
        response = self.conn.get(path = str(url))
        if response.status != 200:
            # Check if "Unothorized" --> raise NotFoundError
            errors_etree = ET.fromstring(response.data)
            for error_etree in errors_etree:
                text = error_etree.text
                if text.lower() == "unauthorized":
                    raise errors.NotFoundError(
                        u"recurring_id: {recurring_id}".format(recurring_id = recurring_id)
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
        tags_etree = ET.fromstring(response.data)

        self.per_page = int(tags_etree.attrib.get("per_page", "0"))
        self.total = int(tags_etree.attrib.get("total", "0"))
        self.page = int(tags_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all tags
        for tag_etree in tags_etree:
            self.append(
                RecurringTag(conn = self.conn, tag_etree = tag_etree)
            )

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                recurring_id = recurring_id,

                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class RecurringTagsIterator(ItemsIterator):
    """
    Iterates over all found tags
    """

    def __init__(self, conn, per_page = 100):
        """
        RecurringTagsIterator
        """

        self.conn = conn
        self.items = RecurringTags(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            recurring_id = None,
            order_by = None,
        )


    def search(
        self,
        recurring_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.recurring_id = recurring_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            recurring_id = self.search_params.recurring_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


