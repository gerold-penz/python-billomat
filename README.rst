##################################
Python Billomat API Client Library
##################################

Billomat (http://www.billomat.com/): Online service
for quoting, billing and more.

Invoices, estimates, reminders, credit notes, order confirmations,
delivery notes,...

The billomat[API] is an open data and programming interface which
enables you to access the data in your Billomat account.

*python-billomat* can be used in Google App Engine (GAE).

- English API Description: http://www.billomat.com/en/api
- Deutsche API Beschreibung: http://www.billomat.com/api


========
Features
========

- Can be used in Google App Engine (GAE)

- Recurrings

  - Recurring-Items
  - Recurring-Tags
  - Recurring-Email-Receivers

- Invoices

  - Invoice-Items
  - Invoice-Tags
  - Invoice-Payments

- Clients

  - Client-Properties
  - Client-Tags

- Contacts

- Articles

  - Article-Properties
  - Article-Tags

- Reminders

  - Reminder-Items
  - Reminder-Tags

- Email-Templates

- Reminder-Texts

- Customfield for metadata for every Billomat object

- Credit-Notes

  - Credit-Note-Items
  - Credit-Note-Tags


============
Installation
============

::

    pip install python-billomat


========
Examples
========

-------
Clients
-------

.. code:: python


    import pybillomat

    conn = pybillomat.Connection(
        billomat_id = "<BillomatId>",
        billomat_api_key = "<BillomatApiKey",
    )


    # Load one client
    client = pybillomat.Client(conn = conn, id = 422909)
    print client
    # --> Client(id=422909, name=u'TESTFIRMA', ...)


    # Iterate over ALL clients.
    # It loads the clients gradually. In pages of 30 clients.
    clients_iterator = pybillomat.ClientsIterator(conn = conn)
    clients_iterator.search()
    for client in clients_iterator:
        assert isinstance(client, pybillomat.Client)
        print client.name


    # Iterate over the first 10 clients
    clients_iterator = pybillomat.ClientsIterator(conn = conn, per_page = 10)
    clients_iterator.search()
    for client in clients_iterator[:10]:
        assert isinstance(client, pybillomat.Client)
        print client.name


    # Create new client
    client = pybillomat.Client.create(
        conn = conn,
        name = u"TEST-CUSTOMER with Umlauts ÖÄÜ",
        zip = u"6020",
        city = u"Innsbruck",
        country_code = u"AT",
        first_name = u"TEST-FIRSTNAME",
        last_name = u"TEST-LASTNAME",
        www = u"http://halvar.at/"
    )
    assert isinstance(client, pybillomat.Client)
    print client.name, unicode(client.id)


--------
Invoices
--------

.. code:: python


    import pybillomat

    conn = pybillomat.Connection(
        billomat_id = "<BillomatId>",
        billomat_api_key = "<BillomatApiKey",
    )


    # Load one invoice
    invoice = pybillomat.Invoice(conn = conn, id = 884447)
    print invoice
    # --> Invoice(address=u'TESTADRESSE', status=u'PAID', ...)


    # Iterate over the last 10 invoices
    invoices_iterator = pybillomat.InvoicesIterator(conn = conn, per_page = 10)
    invoices_iterator.search(order_by = "id DESC")
    for invoice in invoices_iterator[:10]:
        assert isinstance(invoice, pybillomat.Invoice)
        print invoice.invoice_number, invoice.status


    # Iterate over all DRAFT-invoices
    invoices_iterator = pybillomat.InvoicesIterator(conn = conn)
    invoices_iterator.search(status = "DRAFT")
    for invoice in invoices_iterator:
        assert isinstance(invoice, pybillomat.Invoice)
        print invoice.label, repr(invoice.address), invoice.open_amount


    #
    # Iterate over all DRAFT-invoices and complete all of them
    #
    invoices_iterator = pybillomat.InvoicesIterator(conn = conn)

    # Search DRAFT-invoices
    invoices_iterator.search(status = "DRAFT")
    print "Found :", len(invoices_iterator)

    # Complete all DRAFT-invoices
    for invoice in invoices_iterator:
        assert isinstance(invoice, pybillomat.Invoice)
        invoice.complete()

    # Search remaining DRAFT-invoices
    invoices_iterator.search(status = "DRAFT")
    print "Found:", len(invoices_iterator)


========
Licenses
========

- GNU Library or Lesser General Public License (LGPL)
- MIT License 


