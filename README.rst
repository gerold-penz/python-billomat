##################################
Python Billomat API Client Library
##################################


**Pre-Alpha**


Billomat (http://www.billomat.com/): Online service
for quoting, billing and more.

Invoices, estimates, reminders, credit notes, order confirmations,
delivery notes,...

The billomat[API] is an open data and programming interface which
enables you to access the data in your Billomat account.

*python-billomat* is ready to use in Google App Engine (GAE).

- English API Description: http://www.billomat.com/en/api
- Deutsche API Beschreibung: http://www.billomat.com/de/api


========
Features
========

- Google App Engine (GAE) ready

- Recurrings

  - Recurring-Items
  - Recurring-Tags

- Invoices

  - Invoice-Items
  - Invoice-Tags

- Clients

  - Client-Properties
  - Client-Tags

- Article-Tags

- Article-Properties


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
        archived = None,
        number_pre = None,
        number = None,
        number_length = None,
        name = u"TEST-CUSTOMER with Umlauts ÖÄÜ",
        street = None,
        zip = u"6020",
        city = u"Innsbruck",
        state = None,
        country_code = u"AT",
        first_name = u"TEST-FIRSTNAME",
        last_name = u"TEST-LASTNAME",
        salutation = None,
        phone = None,
        fax = None,
        mobile = None,
        email = None,
        www = u"http://halvar.at/",
        tax_number = None,
        vat_number = None,
        bank_account_number = None,
        bank_account_owner = None,
        bank_number = None,
        bank_name = None,
        bank_swift = None,
        bank_iban = None,
        sepa_mandate = None,
        sepa_mandate_date = None,
        tax_rule = None,
        net_gross = None,
        default_payment_types = None,
        note = None,
        discount_rate_type = None,
        discount_rate = None,
        discount_days_type = None,
        discount_days = None,
        due_days_type = None,
        due_days = None,
        reminder_due_days_type = None,
        reminder_due_days = None,
        offer_validity_days_type = None,
        offer_validity_days = None,
        currency_code = None,
        price_group = None
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


