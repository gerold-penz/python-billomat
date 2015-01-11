#!/usr/bin/env python
# coding: utf-8

import pybillomat


# HTTP-Connection to Billomat
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


# Iterate over the last 10 clients
clients_iterator = pybillomat.ClientsIterator(conn = conn, per_page = 10)
clients_iterator.search(order_by = u"id DESC")
for client in clients_iterator[:10]:
    assert isinstance(client, pybillomat.Client)
    print client.name


# Create new client (with all possible parameters)
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


# Create new client (shorter version)
client = pybillomat.Client.create(
    conn = conn,
    name = u"TEST-CUSTOMER 2 with Umlauts ÖÄÜ",
    zip = u"6020",
    city = u"Innsbruck",
    country_code = u"AT",
    first_name = u"TEST-FIRSTNAME",
    last_name = u"TEST-LASTNAME",
    www = u"http://halvar.at/"
)
assert isinstance(client, pybillomat.Client)
print client.name, unicode(client.id)

