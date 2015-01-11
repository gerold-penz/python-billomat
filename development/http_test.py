#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir))
sys.path.insert(0, APPDIR)
import _personal_billomat_data as _personal
# END --- required only for testing, remove in real world code --- END


import pybillomat

conn = pybillomat.Connection(
    billomat_id = _personal.gerolds_billomat_id,
    billomat_api_key = _personal.gerolds_billomat_api_key,
    billomat_app_id = _personal.gerolds_billomat_app_id,
    billomat_app_secret = _personal.gerolds_billomat_app_secret
)

# invoices_iterator = pybillomat.InvoicesIterator(conn = conn)
# invoices_iterator.search()
# for invoice in invoices_iterator:
#     print invoice


# invoice = pybillomat.Invoice.create(
#     conn = conn,
#     client_id = 457179,
#     label = u"Testrechnung von Gerold",
#     payment_types = "BANK_TRANSFER"
# )
#
# invoice_item = pybillomat.InvoiceItem.create(
#     conn = conn,
#     invoice_id = invoice.id,
#     article_id = 115474,
#     quantity = 1,
#     unit_price = 20,
#     title = u"Dös isch a Tescht-Bezeichnung",
#     description = u"Über den Wolken"
# )
#
# pybillomat.InvoiceTag.create(
#     conn = conn,
#     invoice_id = invoice.id,
#     name = u"ÖÄÜ"
# )
#
# invoice.complete(template_id = None)


#
# Rechnung aus Abo-Rechnung erstellen
#
recurring = pybillomat.Recurring(conn = conn, id = 48594)
print "Abo-Rechnung geladen"

recurring_items_iterator = pybillomat.RecurringItemsIterator(conn = conn)
recurring_items_iterator.search(recurring_id = recurring.id)
print "Abo-Rechnung Artikel geladen"

invoice = pybillomat.Invoice.create(
    conn = conn,
    client_id = recurring.client_id,
    contact_id = recurring.contact_id,
    address = recurring.address,
    supply_date = recurring.supply_date,
    supply_date_type = recurring.supply_date_type,
    discount_rate = recurring.discount_rate,
    discount_days = recurring.discount_days,
    label = recurring.label,
    intro = recurring.intro,
    note = recurring.note,
    reduction = recurring.reduction,
    currency_code = recurring.currency_code,
    net_gross = recurring.net_gross,
    quote = recurring.quote,
    payment_types = recurring.payment_types,
    recurring_id = recurring.id
)
print "Rechnung erstellt"

for recurring_item in recurring_items_iterator:
    assert isinstance(recurring_item, pybillomat.RecurringItem)
    invoice_item = pybillomat.InvoiceItem.create(
        conn = conn,
        invoice_id = invoice.id,
        article_id = recurring_item.article_id,
        unit = recurring_item.unit,
        quantity = recurring_item.quantity,
        unit_price = recurring_item.unit_price,
        tax_name = recurring_item.tax_name,
        tax_rate = recurring_item.tax_rate,
        title = recurring_item.title,
        description = recurring_item.description,
        reduction = recurring_item.reduction
    )
    print "Rechnung-Artikel erstellt"

pybillomat.InvoiceTag.create(
    conn = conn,
    invoice_id = invoice.id,
    name = u"TEST"
)
print "Rechnung getaggt"

invoice.complete(template_id = recurring.template_id)
print "Rechnung abgeschlossen"

