#!/usr/bin/env python
# coding: utf-8
"""
Articles

- English API-Description: http://www.billomat.com/en/api/articles
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/artikel
"""

import datetime
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
import errors
from _items_base import Item, ItemsIterator


def _article_xml(
    number_pre = None,
    number = None,
    number_length = None,
    title = None,
    description = None,
    sales_price = None,
    sales_price2 = None,
    sales_price3 = None,
    sales_price4 = None,
    sales_price5 = None,
    currency_code = None,
    unit_id = None,
    tax_id = None,
    purchase_price = None,
    purchase_price_net_gross = None,
    supplier_id = None,
):
    """
    Creates the XML to add or edit a article
    """

    integer_field_names = [
        "number",
        "number_length",
        "unit_id",
        "tax_id",
        "supplier_id",
    ]
    float_fieldnames = [
        "sales_price",
        "sales_price2",
        "sales_price3",
        "sales_price4",
        "sales_price5",
        "purchase_price",
    ]
    string_fieldnames = [
        "number_pre",
        "title",
        "description",
        "currency_code",
        "purchase_price_net_gross",
    ]

    article_tag = ET.Element("article")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            article_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            article_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            article_tag.append(new_tag)

    xml = ET.tostring(article_tag)

    # Finished
    return xml



class Article(Item):

    base_path = u"/api/articles"


    def __init__(self, conn, id = None, article_etree = None):
        """
        Article

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # integer
        self.created = None  # datetime
        self.article_number = None
        self.number = None  # integer
        self.number_pre = None
        self.title = None
        self.description = None
        self.sales_price = None  # float
        self.sales_price2 = None  # float
        self.sales_price3 = None  # float
        self.sales_price4 = None  # float
        self.sales_price5 = None  # float
        self.currency_code = None
        self.unit_id = None  # integer
        self.tax_id = None  # integer
        self.purchase_price = None  # float
        self.purchase_price_net_gross = None
        self.supplier_id = None  # integer

        if article_etree is not None:
            self.load_from_etree(article_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        number_pre = None,
        number = None,
        number_length = None,
        title = None,
        description = None,
        sales_price = None,
        sales_price2 = None,
        sales_price3 = None,
        sales_price4 = None,
        sales_price5 = None,
        currency_code = None,
        unit_id = None,
        tax_id = None,
        purchase_price = None,
        purchase_price_net_gross = None,
        supplier_id = None
    ):
        """
        Creates an article

        :param conn: Connection-Object

        :param number_pre: Prefix
        :param number: Sequential number
        :param number_length: inimum length of the customer number
            (to be filled with leading zeros)
        :param title: Title
        :param description: Description
        :param sales_price: Price
        :param sales_price2: Price for clients which are members of pricegroup 2.
            The normal price is used if no price is defined.
        :param sales_price3: Price for clients which are members of pricegroup 3.
            The normal price is used if no price is defined.
        :param sales_price4: Price for clients which are members of pricegroup 4.
            The normal price is used if no price is defined.
        :param sales_price5: Price for clients which are members of pricegroup 5.
            The normal price is used if no price is defined.
        :param currency_code: Currency
        :param unit_id: ID of the chosen unit
        :param tax_id: ID of the chosen tax rate
        :param purchase_price: Purchase price
        :param purchase_price_net_gross: Price basis of purchase price
            (gross or net prices). Possible values: "NET", "GROSS"
        :param supplier_id: ID of the chosen supplier
        """

        # XML
        xml = _article_xml(
            number_pre = number_pre,
            number = number,
            number_length = number_length,
            title = title,
            description = description,
            sales_price = sales_price,
            sales_price2 = sales_price2,
            sales_price3 = sales_price3,
            sales_price4 = sales_price4,
            sales_price5 = sales_price5,
            currency_code = currency_code,
            unit_id = unit_id,
            tax_id = tax_id,
            purchase_price = purchase_price,
            purchase_price_net_gross = purchase_price_net_gross,
            supplier_id = supplier_id
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))
    
        # Create Article-Object
        article = cls(conn = conn)
        article.content_language = response.headers.get("content-language", None)
        article.load_from_xml(response.data)
    
        # Finished
        return article
    
    
    def edit(
        self,
        id = None,
        number_pre = None,
        number = None,
        number_length = None,
        title = None,
        description = None,
        sales_price = None,
        sales_price2 = None,
        sales_price3 = None,
        sales_price4 = None,
        sales_price5 = None,
        currency_code = None,
        unit_id = None,
        tax_id = None,
        purchase_price = None,
        purchase_price_net_gross = None,
        supplier_id = None
    ):
        """
        Edit an article

        :param id: ID of the article

        :param number_pre: Prefix
        :param number: Sequential number
        :param number_length: inimum length of the customer number
            (to be filled with leading zeros)
        :param title: Title
        :param description: Description
        :param sales_price: Price
        :param sales_price2: Price for clients which are members of pricegroup 2.
            The normal price is used if no price is defined.
        :param sales_price3: Price for clients which are members of pricegroup 3.
            The normal price is used if no price is defined.
        :param sales_price4: Price for clients which are members of pricegroup 4.
            The normal price is used if no price is defined.
        :param sales_price5: Price for clients which are members of pricegroup 5.
            The normal price is used if no price is defined.
        :param currency_code: Currency
        :param unit_id: ID of the chosen unit
        :param tax_id: ID of the chosen tax rate
        :param purchase_price: Purchase price
        :param purchase_price_net_gross: Price basis of purchase price
            (gross or net prices). Possible values: "NET", "GROSS"
        :param supplier_id: ID of the chosen supplier
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _article_xml(
            number_pre = number_pre,
            number = number,
            number_length = number_length,
            title = title,
            description = description,
            sales_price = sales_price,
            sales_price2 = sales_price2,
            sales_price3 = sales_price3,
            sales_price4 = sales_price4,
            sales_price5 = sales_price5,
            currency_code = currency_code,
            unit_id = unit_id,
            tax_id = tax_id,
            purchase_price = purchase_price,
            purchase_price_net_gross = purchase_price_net_gross,
            supplier_id = supplier_id
        )

        # Path
        path = "/api/articles/{id}".format(id = self.id)

        # Send PUT-request
        response = self.conn.put(path = path, body = xml)
        if response.status != 200:  # Edited
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))


    # def get_tags(self):
    #     """
    #     Gibt eine Liste mit Schlagworten des Artikels zurück
    #     """
    #
    #     # Parameters
    #     if not self.id:
    #         raise errors.NoIdError()
    #     ...


class Articles(list):

    def __init__(self, conn):
        """
        Articles-List

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
        article_number = None,
        title = None,
        description = None,
        currency_code = None,
        unit_id = None,
        tags = None,
        supplier_id = None,

        order_by = None,
        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with Article-objects

        If no search criteria given --> all articles will returned (REALLY ALL!).

        :param article_number: Article number
        :param title: Title
        :param description: Description
        :param currency_code: ISO code of the currency
        :param unit_id: ID of the chosen unit
        :param tags: Comma seperated list of tags
        :param supplier_id: ID of the chosen supplier

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        :param allow_empty_filter: If `True`, every filter-parameter may be empty.
            So, all articles will returned. !!! EVERY INVOICE !!!
        """
        
        # Check empty filter
        if not allow_empty_filter:
            if not any([
                article_number,
                title,
                description,
                currency_code,
                unit_id,
                tags,
                supplier_id,
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
        url = Url(path = "/api/articles")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameters
        if article_number:
            url.query["article_number"] = article_number
        if title:
            url.query["title"] = title
        if description:
            url.query["description"] = description
        if currency_code:
            url.query["currency_code"] = currency_code
        if unit_id:
            url.query["unit_id"] = unit_id
        if tags:
            url.query["tags"] = tags
        if supplier_id:
            url.query["supplier_id"] = supplier_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        articles_etree = ET.fromstring(response.data)

        self.per_page = int(articles_etree.attrib.get("per_page", "100"))
        self.total = int(articles_etree.attrib.get("total", "0"))
        self.page = int(articles_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all articles
        for article_etree in articles_etree:
            self.append(Article(conn = self.conn, article_etree = article_etree))

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                article_number = article_number,
                title = title,
                description = description,
                currency_code = currency_code,
                unit_id = unit_id,
                tags = tags,
                supplier_id = supplier_id,

                order_by = order_by,
                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class ArticlesIterator(ItemsIterator):
    """
    Iterates over all found articles
    """

    def __init__(self, conn, per_page = 30):
        """
        ArticlesIterator
        """

        self.conn = conn
        self.items = Articles(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            article_number = None,
            title = None,
            description = None,
            currency_code = None,
            unit_id = None,
            tags = None,
            supplier_id = None,
            order_by = None,
        )


    def search(
        self,
        article_number = None,
        title = None,
        description = None,
        currency_code = None,
        unit_id = None,
        tags = None,
        supplier_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.article_number = article_number
        self.search_params.title = title
        self.search_params.description = description
        self.search_params.currency_code = currency_code
        self.search_params.unit_id = unit_id
        self.search_params.tags = tags
        self.search_params.supplier_id = supplier_id
        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            article_number = self.search_params.article_number,
            title = self.search_params.title,
            description = self.search_params.description,
            currency_code = self.search_params.currency_code,
            unit_id = self.search_params.unit_id,
            tags = self.search_params.tags,
            supplier_id = self.search_params.supplier_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )


