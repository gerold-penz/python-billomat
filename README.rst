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

--------------
Get one client
--------------

.. code:: python

    import pybillomat

    conn = pybillomat.Connection(
        billomat_id = "<BillomatId>",
        billomat_api_key = "<BillomatApiKey",
    )

    client = pybillomat.Client(conn = conn)
    client.load(id = 422909)
    print client
    # --> Client(
    #     id=422909,
    #     client_number=u'K10141005',
    #     created=datetime.datetime(2014, 10, 27, 11, 24, 49),
    #     name=u'TESTFIRMA',
    #     first_name=u'TESTVORNAME',
    #     last_name=u'TESTNACHNAME',
    #     ...
    # )


------------------------
Iterate over all clients
------------------------

.. code:: python


    import pybillomat

    conn = pybillomat.Connection(
        billomat_id = "<BillomatId>",
        billomat_api_key = "<BillomatApiKey",
    )


    # This example iterates over ALL clients. It loads the clients gradually.
    # In pages of 30 clients.

    clients = pybillomat.ClientsIterator(conn = conn, per_page = 30)
    clients.search()

    for client in clients:
        assert isinstance(client, pybillomat.Client)
        print client.name

    print len(clients)


========
Licenses
========

- GNU Library or Lesser General Public License (LGPL)
- MIT License 


