#!/usr/bin/env python
# coding: utf-8
"""
Recurring-Items

- English API-Description: http://www.billomat.com/en/api/recurrings/items
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/abo-rechnungen/positionen
"""


import errors
import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
from _items_base import Item, ItemsIterator


def _recurring_item_xml(
    recurring_id = None,
    article_id = None,
    unit = None,
    quantity = None,
    unit_price = None,
    tax_name = None,
    tax_rate = None,
    title = None,
    description = None,
    reduction = None
):
    """
    Creates the XML to add or edit a recurring-item
    """

    integer_field_names = [
        "recurring_id",
        "article_id",
    ]
    float_fieldnames = [
        "quantity",
        "unit_price",
        "tax_rate",
    ]
    string_fieldnames = [
        "unit",
        "tax_name",
        "title",
        "description",
        "reduction",
    ]

    recurring_item_tag = ET.Element("recurring-item")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            recurring_item_tag.append(new_tag)

    # Float Fields
    for field_name in float_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(float(value))
            recurring_item_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            recurring_item_tag.append(new_tag)

    xml = ET.tostring(recurring_item_tag)

    # Finished
    return xml


class RecurringItem(Item):

    base_path = u"/api/recurring-items"


    def __init__(self, conn, id = None, recurring_item_etree = None):
        """
        Recurring-Item

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn

        self.id = id  # integer
        self.created = None  # datetime
        self.article_id = None
        self.recurring_id = None  # integer
        self.position = None  # integer
        self.unit = None
        self.quantity = None  # float
        self.unit_price = None  # float
        self.tax_name = None
        self.tax_rate = None  # float
        self.title = None
        self.description = None
        self.total_gross = None  # float
        self.total_net = None  # float
        self.reduction = None
        self.total_gross_unreduced = None  # float
        self.total_net_unreduced = None  # float

        if recurring_item_etree is not None:
            self.load_from_etree(recurring_item_etree)


    @classmethod
    def create(
        cls,
        conn,
        recurring_id = None,
        article_id = None,
        unit = None,
        quantity = None,
        unit_price = None,
        tax_name = None,
        tax_rate = None,
        title = None,
        description = None,
        reduction = None
    ):
        """
        Creates a recurring-item

        :param conn: Connection-Object

        :param recurring_id: ID of the recurring
        :param article_id: ID of the article, sets additionally the values
            from the article on creation
        :param unit: Unit
        :param quantity: Quantity
        :param unit_price: Price per unit
        :param tax_name: Name of the tax
        :param tax_rate: rate of taxation
        :param title: Title
        :param description: Description
        :param reduction: Reduction (absolute or percent: 10/10%)
        """

        # XML
        xml = _recurring_item_xml(
            recurring_id = recurring_id,
            article_id = article_id,
            unit = unit,
            quantity = quantity,
            unit_price = unit_price,
            tax_name = tax_name,
            tax_rate = tax_rate,
            title = title,
            description = description,
            reduction = reduction
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))

        # Create Recurring-Object
        recurring = cls(conn = conn)
        recurring.content_language = response.headers.get("content-language", None)
        recurring.load_from_xml(response.data)

        # Finished
        return recurring


#     def edit(
#         self,
#         id = None,
#         client_id = None,
#         contact_id = None,
#         title = None,
#         address = None,
#         supply_date = None,
#         supply_date_type = None,
#         due_days = None,
#         discount_rate = None,
#         discount_days = None,
#         name = None,
#         label = None,
#         intro = None,
#         note = None,
#         currency_code = None,
#         reduction = None,
#         net_gross = None,
#         quote = None,
#         payment_types = None,
#         action = None,
#         cycle_number = None,
#         cycle = None,
#         hour = None,
#         start_date = None,
#         end_date = None,
#         next_creation_date = None,
#         email_sender = None,
#         email_subject = None,
#         email_message = None,
#         email_filename = None,
#         offer_id = None,
#         confirmation_id = None,
#         template_id = None
#     ):
#         """
#         Edit a recurring
#
#         :param id: ID of the recurring
#         :param client_id: ID of the client
#         :param contact_id: ID of the contact
#         :param title: Document title; Let it empty to use the default value
#             from settings: "Invoice [Invoice.invoice_number]"
#         :param address: the address;
#             Pass an empty value to use the current customer address.
#         :param supply_date: supply/delivery date; MIXED (DATE/ALNUM)
#         :param supply_date_type: type or supply/delivery date; ALNUM (
#             "SUPPLY_DATE", "DELIVERY_DATE", "SUPPLY_TEXT", "DELIVERY_TEXT")
#         :param due_days: Due days
#         :param discount_rate: Cash discount
#         :param discount_days: Cash discount days
#         :param name: Name of the recurring; is the title of the recurring
#         :param label: Label text to describe the project
#         :param intro: Introductory text; Default value taken from the settings
#         :param note: Explanatory notes; Default value taken from the settings
#         :param reduction: Reduction (absolute or percent: 10/10%)
#         :param currency_code: Currency; ISO currency code
#         :param net_gross: Price basis (gross or net prices)
#         :param quote: Currency quote (for conversion into standard currency)
#         :param payment_types: List (separated by comma) of all accepted payment
#             types.
#         :param action: Action to be executed (CREATE, COMPLETE, EMAIL)
#         :param cycle_number: Number of intervals. For example, 3 for
#             "every 3 months"
#         :param cycle: Interval (DAILY, WEEKLY, MONTHLY, YEARLY)
#         :param hour: Time of Day (hour)
#         :param start_date: Start date;
#         :param end_date: End date
#         :param next_creation_date: Date of the next creation;
#             Put "" (empty string) to set recurring inactive.
#         :param email_sender: Sender when sending e-mail. If you pass an empty
#             value, the sender will be used from the settings.
#         :param email_subject: Subject when sending e-mail. If you pass an
#             empty value, the subject will be used from the settings.
#         :param email_message: Message text when sending e-mail. If you pass
#             an empty value, the message will be used from the settings.
#         :param email_filename: Filename of the invoice when sending e-mail.
#             If you pass an empty value, the filename will be used from the settings.
#         :param offer_id: The ID of the estimate, if the recurring was created
#             from an estimate.
#         :param confirmation_id: The ID of the confirmation, if the recurring
#             was created from a confirmation.
#         :param template_id: Template ID
#         """
#
#         # Parameters
#         if id:
#             self.id = id
#         if not self.id:
#             raise errors.NoIdError()
#
#         # XML
#         xml = _recurring_xml(
#             client_id = client_id,
#             contact_id = contact_id,
#             title = title,
#             address = address,
#             supply_date = supply_date,
#             supply_date_type = supply_date_type,
#             due_days = due_days,
#             discount_rate = discount_rate,
#             discount_days = discount_days,
#             name = name,
#             label = label,
#             intro = intro,
#             note = note,
#             currency_code = currency_code,
#             reduction = reduction,
#             net_gross = net_gross,
#             quote = quote,
#             payment_types = payment_types,
#             action = action,
#             cycle_number = cycle_number,
#             cycle = cycle,
#             hour = hour,
#             start_date = start_date,
#             end_date = end_date,
#             next_creation_date = next_creation_date,
#             email_sender = email_sender,
#             email_subject = email_subject,
#             email_message = email_message,
#             email_filename = email_filename,
#             offer_id = offer_id,
#             confirmation_id = confirmation_id,
#             template_id = template_id
#         )
#
#         # Path
#         path = "/api/recurrings/{id}".format(id = self.id)
#
#         # Send PUT-request
#         response = self.conn.put(path = path, body = xml)
#         if response.status != 200:  # Edited
#             raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))
#
#
# class Recurrings(list):
#
#     def __init__(self, conn):
#         """
#         Recurrings-List
#
#         :param conn: Connection-Object
#         """
#
#         list.__init__(self)
#
#         self.conn = conn
#         self.per_page = None
#         self.total = None
#         self.page = None
#         self.pages = None
#
#
#     def search(
#         self,
#         # Search parameters
#         client_id = None,
#         contact_id = None,
#         name = None,
#         payment_type = None,
#         cycle = None,
#         label = None,
#         intro = None,
#         note = None,
#         tags = None,
#
#         order_by = None,
#         fetch_all = False,
#         allow_empty_filter = False,
#         keep_old_items = False,
#         page = 1,
#         per_page = None
#     ):
#         """
#         Fills the list with Recurring-objects
#
#         If no search criteria given --> all recurrings will returned (REALLY ALL!).
#
#         :param client_id: ID of the client
#         :param contact_id: ID of the contact
#         :param name: The Name of the recurring
#         :param payment_type: Payment Type (eg. CASH, BANK_TRANSFER, PAYPAL, ...).
#             More than one payment type could be given as a comma separated list.
#             Theses payment types will be logically OR-connected.
#             You can find a overview of all payment types at API documentation
#             of payments.
#         :param cycle: Interval (DAILY, WEEKLY, MONTHLY, YEARLY).
#         :param label: Free text search in label text
#         :param intro: Free text search in introductory text
#         :param note: Free text search in explanatory notes
#         :param tags: Comma seperated list of tags
#
#         :param order_by: Sortings consist of the name of the field and
#             sort order: ASC for ascending resp. DESC for descending order.
#             If no order is specified, ascending order (ASC) is used.
#             Nested sort orders are possible. Please separate the sort orders by
#             comma.
#
#         :param allow_empty_filter: If `True`, every filter-parameter may be empty.
#             So, all invoices will returned. !!! EVERY INVOICE !!!
#         """
#
#         # Check empty filter
#         if not allow_empty_filter:
#             if not any([
#                 client_id,
#                 contact_id,
#                 name,
#                 payment_type,
#                 cycle,
#                 label,
#                 intro,
#                 note,
#                 tags,
#             ]):
#                 raise errors.EmptyFilterError()
#
#         # Empty the list
#         if not keep_old_items:
#             while True:
#                 try:
#                     self.pop()
#                 except IndexError:
#                     break
#
#         # Url and system-parameters
#         url = Url(path = "/api/recurrings")
#         url.query["page"] = page
#         if per_page:
#             url.query["per_page"] = per_page
#         if order_by:
#             url.query["order_by"] = order_by
#
#         # Search parameters
#         if client_id:
#             url.query["client_id"] = client_id
#         if contact_id:
#             url.query["contact_id"] = contact_id
#         if name:
#             url.query["name"] = name
#         if payment_type:
#             url.query["payment_type"] = payment_type
#         if cycle:
#             url.query["cycle"] = cycle
#         if label:
#             url.query["label"] = label
#         if intro:
#             url.query["intro"] = intro
#         if note:
#             url.query["note"] = note
#         if tags:
#             url.query["tags"] = tags
#
#         # Fetch data
#         response = self.conn.get(path = str(url))
#
#         # Parse XML
#         recurrings_etree = ET.fromstring(response.data)
#
#         self.per_page = int(recurrings_etree.attrib.get("per_page", "100"))
#         self.total = int(recurrings_etree.attrib.get("total", "0"))
#         self.page = int(recurrings_etree.attrib.get("page", "1"))
#         self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
#
#         # Iterate over all recurrings
#         for recurring_etree in recurrings_etree:
#             self.append(Recurring(conn = self.conn, recurring_etree = recurring_etree))
#
#         # Fetch all
#         if fetch_all and self.total > (self.page * self.per_page):
#             self.search(
#                 # Search parameters
#                 client_id = client_id,
#                 contact_id = contact_id,
#                 name = name,
#                 payment_type = payment_type,
#                 cycle = cycle,
#                 label = label,
#                 intro = intro,
#                 note = note,
#                 tags = tags,
#
#                 order_by = order_by,
#                 fetch_all = fetch_all,
#                 allow_empty_filter = allow_empty_filter,
#                 keep_old_items = True,
#                 page = page + 1,
#                 per_page = per_page
#             )
#
#
# class RecurringsIterator(ItemsIterator):
#     """
#     Iterates over all found recurrings
#     """
#
#     def __init__(self, conn, per_page = 30):
#         """
#         RecurringsIterator
#         """
#
#         self.conn = conn
#         self.items = Recurrings(self.conn)
#         self.per_page = per_page
#         self.search_params = Bunch(
#             client_id = None,
#             contact_id = None,
#             name = None,
#             payment_type = None,
#             cycle = None,
#             label = None,
#             intro = None,
#             note = None,
#             tags = None,
#             order_by = None
#         )
#
#
#     def search(
#         self,
#         client_id = None,
#         contact_id = None,
#         name = None,
#         payment_type = None,
#         cycle = None,
#         label = None,
#         intro = None,
#         note = None,
#         tags = None,
#         order_by = None
#     ):
#         """
#         Search
#         """
#
#         # Params
#         self.search_params.client_id = client_id
#         self.search_params.contact_id = contact_id
#         self.search_params.name = name
#         self.search_params.payment_type = payment_type
#         self.search_params.cycle = cycle
#         self.search_params.label = label
#         self.search_params.intro = intro
#         self.search_params.note = note
#         self.search_params.tags = tags
#         self.search_params.order_by = order_by
#
#         # Search and prepare first page as result
#         self.load_page(1)
#
#
#     def load_page(self, page):
#
#         self.items.search(
#             client_id = self.search_params.client_id,
#             contact_id = self.search_params.contact_id,
#             name = self.search_params.name,
#             payment_type = self.search_params.payment_type,
#             cycle = self.search_params.cycle,
#             label = self.search_params.label,
#             intro = self.search_params.intro,
#             note = self.search_params.note,
#             tags = self.search_params.tags,
#             order_by = self.search_params.order_by,
#
#             fetch_all = False,
#             allow_empty_filter = True,
#             keep_old_items = False,
#             page = page,
#             per_page = self.per_page
#         )
#
#
