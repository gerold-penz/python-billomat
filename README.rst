##################################
Python Billomat API Client Library
##################################

Billomat (http://www.billomat.com/): Online service
for quoting, billing and more.

Invoices, estimates, reminders, credit notes, order confirmations,
delivery notes,...

The billomat[API] is an open data and programming interface which
enables you to access the data in your Billomat account.

- English API Description: http://www.billomat.com/en/api
- Deutsche API Beschreibung: http://www.billomat.com/de/api


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
    client = pybillomat.Client(conn = conn)
    client.load(id = 422909)
    print client
    # --> Client(id=422909, name=u'TESTFIRMA', ...)


    # Load all clients into memory
    # WARNING! This example loads ALL (really ALL) clients into memory
    clients = pybillomat.Clients(conn = conn)
    clients.search(fetch_all = True, allow_empty_filter = True)
    for client in clients:
        assert isinstance(client, pybillomat.Client)
        print client.name


    # This example iterates over ALL clients. It loads the clients gradually. In
    # pages of 30 clients.
    clients_iterator = pybillomat.ClientsIterator(conn = conn, per_page = 30)
    clients_iterator.search()
    for client in clients_iterator:
        assert isinstance(client, pybillomat.Client)
        print client.name


    # Iterate over the first 10 clients (5 per page)
    clients_iterator = pybillomat.ClientsIterator(conn = conn, per_page = 5)
    clients_iterator.search()
    for client in clients_iterator[:10]:
        assert isinstance(client, pybillomat.Client)
        print client.name


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
    invoice = pybillomat.Invoice(conn = conn)
    invoice.load(id = 884447)
    print invoice
    # --> Invoice(address=u'TESTADRESSE', status=u'PAID', ...)


    # Iterate over the last 10 invoices (5 per page)
    invoices_iterator = pybillomat.InvoicesIterator(conn = conn, per_page = 5)
    invoices_iterator.search()
    for invoice in invoices_iterator[-10:]:
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


