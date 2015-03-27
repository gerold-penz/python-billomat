#!/usr/bin/env python
# coding: utf-8
"""
Mahnungen

- English API-Description: http://www.billomat.com/en/api/reminders
- Deutsche API-Beschreibung: http://www.billomat.com/de/api/mahnungen
"""

import xml.etree.ElementTree as ET
from bunch import Bunch
from http import Url
import errors
from _items_base import Item, ItemsIterator


def _reminder_xml(
    invoice_id = None,  # integer
    contact_id = None,  # integer
    address = None,
    date = None,  # date
    due_date = None,  # date
    subject = None,
    label = None,
    intro = None,
    note = None,
):
    """
    Creates the XML to add or edit a reminder
    """

    integer_field_names = [
        "invoice_id",
        "contact_id",
    ]
    date_fieldnames = [
        "date",
        "due_date",
    ]
    string_fieldnames = [
        "address",
        "subject",
        "label",
        "intro",
        "note",
    ]

    reminder_tag = ET.Element("reminder")

    # Integer Fields
    for field_name in integer_field_names:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(int(value))
            reminder_tag.append(new_tag)

    # Date fields
    for field_name in date_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = value.isoformat()
            reminder_tag.append(new_tag)

    # String Fields
    for field_name in string_fieldnames:
        value = locals()[field_name]
        if value is not None:
            new_tag = ET.Element(field_name)
            new_tag.text = unicode(value)
            reminder_tag.append(new_tag)

    xml = ET.tostring(reminder_tag)

    # Finished
    return xml


class Reminder(Item):

    base_path = u"/api/reminders"


    def __init__(self, conn, id = None, reminder_etree = None):
        """
        Reminder

        :param conn: Connection-Object
        """

        Bunch.__init__(self)

        self.conn = conn
        self.content_language = None

        self.id = id  # integer
        self.created = None  # datetime
        self.status = None
        self.invoice_id = None  # integer
        self.contact_id = None  # integer
        self.reminder_text_id = None  # integer
        self.reminder_level = None  # integer
        self.reminder_level_name = None
        self.date = None  # date
        self.label = None
        self.subject = None
        self.intro = None
        self.note = None
        self.due_date = None  # date
        self.total_gross = None  # float
        self.is_old = None  # Steht dieses Flag auf 1, dann gibt es eine aktuellere Mahnung.

        if reminder_etree is not None:
            self.load_from_etree(reminder_etree)
        elif id is not None:
            self.load()


    @classmethod
    def create(
        cls,
        conn,
        invoice_id = None,
        contact_id = None,
        address = None,
        date = None,
        due_date = None,
        subject = None,
        label = None,
        intro = None,
        note = None
    ):
        """
        Creates a reminder

        :param conn: Connection-Object

        :param invoice_id: ID of the overdue invoice
        :param contact_id: ID of the contact
        :param address: the address;
            Default: Address from invoice
        :param date: Date of the reminder; Default: today
        :param due_date: Due date of the reminder;
            Default: date + due days taken from the settings
        :param subject: Subject;
            Default: Subject of the next dunning level (if available)
        :param label: Label text to describe the project
        :param intro: Introductory text;
            Default: Introductory text of the next dunning level (if available)
        :param note: Explanatory notes;
            Default: Explanatory notes of the next dunning level (if available)
        """

        # XML
        xml = _reminder_xml(
            invoice_id = invoice_id,
            contact_id = contact_id,
            address = address,
            date = date,
            due_date = due_date,
            subject = subject,
            label = label,
            intro = intro,
            note = note
        )

        # Send POST-request
        response = conn.post(path = cls.base_path, body = xml)
        if response.status != 201:  # Created
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))
    
        # Create Reminder-Object
        reminder = cls(conn = conn)
        reminder.content_language = response.headers.get("content-language", None)
        reminder.load_from_xml(response.data)
    
        # Finished
        return reminder
    
    
    def edit(
        self,
        id = None,
        invoice_id = None,
        contact_id = None,
        address = None,
        date = None,
        due_date = None,
        subject = None,
        label = None,
        intro = None,
        note = None
    ):
        """
        Edit a reminder

        :param id: ID of the reminder

        :param invoice_id: ID of the overdue invoice
        :param contact_id: ID of the contact
        :param address: the address;
            Default: Address from invoice
        :param date: Date of the reminder; Default: today
        :param due_date: Due date of the reminder;
            Default: date + due days taken from the settings
        :param subject: Subject;
            Default: Subject of the next dunning level (if available)
        :param label: Label text to describe the project
        :param intro: Introductory text;
            Default: Introductory text of the next dunning level (if available)
        :param note: Explanatory notes;
            Default: Explanatory notes of the next dunning level (if available)
        """

        # Parameters
        if id:
            self.id = id
        if not self.id:
            raise errors.NoIdError()

        # XML
        xml = _reminder_xml(
            invoice_id = invoice_id,
            contact_id = contact_id,
            address = address,
            date = date,
            due_date = due_date,
            subject = subject,
            label = label,
            intro = intro,
            note = note
        )

        # Path
        path = "/api/reminders/{id}".format(id = self.id)

        # Send PUT-request
        response = self.conn.put(path = path, body = xml)
        if response.status != 200:  # Edited
            raise errors.BillomatError(unicode(response.data, encoding = "utf-8"))


    def complete(self, template_id = None):
        """
        Closes a reminder in the draft status (DRAFT).
        Here, the status of open (OPEN) or overdue (Overdue) is set and
        a PDF is generated and stored in the file system.
        The optional paramter template_id determines which template is used
        to create a pdf. If this parameter is not specified, the default
        template set is used.
        """

        # Path
        path = "/api/reminders/{id}/complete".format(id = self.id)

        # XML
        complete_tag = ET.Element("complete")
        if template_id:
            template_id_tag = ET.Element("template_id")
            template_id_tag.text = str(template_id)
            complete_tag.append(template_id_tag)
        xml = ET.tostring(complete_tag)

        # Send PUT-request
        response = self.conn.put(path = path, body = xml)

        if response.status != 200:
            # Parse response
            error_text_list = []
            for error in ET.fromstring(response.data):
                error_text_list.append(error.text)

            # Raise Error
            raise errors.BillomatError("\n".join(error_text_list))


    def send(
        self,
        from_address = None,
        to_address = None,
        cc_address = None,
        bcc_address = None,
        subject = None,
        body = None,
        filename = None,
        # attachments = None
    ):
        """
        Sends the reminder per e-mail to the customer

        :param from_address: (originally: from) Sender
        :param to_address: (originally: recepients)
        :param cc_address: (originally: recepients)
        :param bcc_address: (originally: recepients)
        :param subject: Subject of the e-mail (may include placeholders)
        :param body: Text of the e-mail (may include placeholders)
        :param filename: Name of the PDF file (without .pdf)
        # :param attachments: List with Dictionaries::
        #
        #     [
        #         {
        #             "filename": "<Filename>",
        #             "mimetype": "<MimeType>",
        #             "base64file": "<Base64EncodedFile>"
        #         },
        #         ...
        #     ]
        """

        # Path
        path = "{base_path}/{id}/email".format(
            base_path = self.base_path,
            id = self.id
        )

        # XML
        email_tag = ET.Element("email")

        # From
        if from_address:
            from_tag = ET.Element("from")
            from_tag.text = from_address
            email_tag.append(from_tag)

        # Recipients
        if to_address or cc_address or bcc_address:
            recipients_tag = ET.Element("recipients")
            email_tag.append(recipients_tag)

            # To
            if to_address:
                to_tag = ET.Element("to")
                to_tag.text = to_address
                recipients_tag.append(to_tag)

            # Cc
            if cc_address:
                cc_tag = ET.Element("cc")
                cc_tag.text = cc_address
                recipients_tag.append(cc_tag)

            # Bcc
            if bcc_address:
                bcc_tag = ET.Element("bcc")
                bcc_tag.text = bcc_address
                recipients_tag.append(bcc_tag)

        # Subject
        if subject:
            subject_tag = ET.Element("subject")
            subject_tag.text = subject
            email_tag.append(subject_tag)

        # Body
        if body:
            body_tag = ET.Element("body")
            body_tag.text = body
            email_tag.append(body_tag)

        # Filename
        if filename:
            filename_tag = ET.Element("filename")
            filename_tag.text = filename
            filename_tag.append(filename_tag)

        # ToDo: Attachments

        xml = ET.tostring(email_tag)

        # Send POST-request
        response = self.conn.post(path = path, body = xml)

        if response.status != 200:
            # Parse response
            error_text_list = []
            for error in ET.fromstring(response.data):
                error_text_list.append(error.text)

            # Raise Error
            raise errors.BillomatError("\n".join(error_text_list))


class Reminders(list):

    def __init__(self, conn):
        """
        Reminders-List

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
        contact_id = None,
        invoice_number = None,
        status = None,
        from_date = None,
        to_date = None,
        subject = None,
        label = None,
        intro = None,
        note = None,
        tags = None,
        article_id = None,

        order_by = None,
        fetch_all = False,
        allow_empty_filter = False,
        keep_old_items = False,
        page = 1,
        per_page = None
    ):
        """
        Fills the list with Reminder-objects

        If no search criteria given --> all reminders will returned (REALLY ALL!).

        :param client_id: ID of the client
        :param contact_id: ID of the contact
        :param invoice_number: Number of the related invoice
        :param status: Status (DRAFT, OPEN, PAID, OVERDUE, CANCELED).
            More than one statuses could be given as a comma separated list.
            Theses statuses will be logically OR-connected.
        :param from_date: Only show invoices since this date
        :param to_date: Only show invoices up to this date
        :param subject: Free text search in subject
        :param label: Free text search in label text
        :param intro: Free text search in introductory text
        :param note: Free text search in explanatory notes
        :param tags: Comma seperated list of tags
        :param article_id: ID of an article

        :param order_by: Sortings consist of the name of the field and
            sort order: ASC for ascending resp. DESC for descending order.
            If no order is specified, ascending order (ASC) is used.
            Nested sort orders are possible. Please separate the sort orders by
            comma.

        :param allow_empty_filter: If `True`, every filter-parameter may be empty.
            So, all reminders will returned. !!! EVERY !!!
        """
        
        # Check empty filter
        if not allow_empty_filter:
            if not any([
                client_id,
                contact_id,
                invoice_number,
                status,
                from_date,
                to_date,
                subject,
                label,
                intro,
                note,
                tags,
                article_id,
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
        url = Url(path = "/api/reminders")
        url.query["page"] = page
        if per_page:
            url.query["per_page"] = per_page
        if order_by:
            url.query["order_by"] = order_by

        # Search parameters
        if client_id:
            url.query["client_id"] = client_id
        if contact_id:
            url.query["contact_id"] = contact_id
        if invoice_number:
            url.query["invoice_number"] = invoice_number
        if status:
            url.query["status"] = status
        if from_date:
            url.query["from_date"] = from_date.isoformat()
        if to_date:
            url.query["to_date"] = to_date.isoformat()
        if subject:
            url.query["subject"] = subject
        if label:
            url.query["label"] = label
        if intro:
            url.query["intro"] = intro
        if note:
            url.query["note"] = note
        if tags:
            url.query["tags"] = tags
        if article_id:
            url.query["article_id"] = article_id

        # Fetch data
        response = self.conn.get(path = str(url))

        # Parse XML
        reminders_etree = ET.fromstring(response.data)

        self.per_page = int(reminders_etree.attrib.get("per_page", "100"))
        self.total = int(reminders_etree.attrib.get("total", "0"))
        self.page = int(reminders_etree.attrib.get("page", "1"))
        try:
            self.pages = (self.total // self.per_page) + int(bool(self.total % self.per_page))
        except ZeroDivisionError:
            self.pages = 0

        # Iterate over all reminders
        for reminder_etree in reminders_etree:
            self.append(Reminder(conn = self.conn, reminder_etree = reminder_etree))

        # Fetch all
        if fetch_all and self.total > (self.page * self.per_page):
            self.search(
                # Search parameters
                client_id = client_id,
                contact_id = contact_id,
                invoice_number = invoice_number,
                status = status,
                from_date = from_date,
                to_date = to_date,
                subject = subject,
                label = label,
                intro = intro,
                note = note,
                tags = tags,
                article_id = article_id,

                order_by = order_by,
                fetch_all = fetch_all,
                allow_empty_filter = allow_empty_filter,
                keep_old_items = True,
                page = page + 1,
                per_page = per_page
            )


class RemindersIterator(ItemsIterator):
    """
    Iterates over all found reminders
    """

    def __init__(self, conn, per_page = 30):
        """
        RemindersIterator
        """

        self.conn = conn
        self.items = Reminders(self.conn)
        self.per_page = per_page
        self.search_params = Bunch(
            client_id = None,
            contact_id = None,
            invoice_number = None,
            status = None,
            from_date = None,
            to_date = None,
            subject = None,
            label = None,
            intro = None,
            note = None,
            tags = None,
            article_id = None,

            order_by = None,
        )


    def search(
        self,
        client_id = None,
        contact_id = None,
        invoice_number = None,
        status = None,
        from_date = None,
        to_date = None,
        subject = None,
        label = None,
        intro = None,
        note = None,
        tags = None,
        article_id = None,
        order_by = None
    ):
        """
        Search
        """

        # Params
        self.search_params.client_id = client_id
        self.search_params.contact_id = contact_id
        self.search_params.invoice_number = invoice_number
        self.search_params.status = status
        self.search_params.from_date = from_date
        self.search_params.to_date = to_date
        self.search_params.subject = subject
        self.search_params.label = label
        self.search_params.intro = intro
        self.search_params.note = note
        self.search_params.tags = tags
        self.search_params.article_id = article_id

        self.search_params.order_by = order_by

        # Search and prepare first page as result
        self.load_page(1)


    def load_page(self, page):

        self.items.search(
            client_id = self.search_params.client_id,
            contact_id = self.search_params.contact_id,
            invoice_number = self.search_params.invoice_number,
            status = self.search_params.status,
            from_date = self.search_params.from_date,
            to_date = self.search_params.to_date,
            subject = self.search_params.subject,
            label = self.search_params.label,
            intro = self.search_params.intro,
            note = self.search_params.note,
            tags = self.search_params.tags,
            article_id = self.search_params.article_id,
            order_by = self.search_params.order_by,

            fetch_all = False,
            allow_empty_filter = True,
            keep_old_items = False,
            page = page,
            per_page = self.per_page
        )
