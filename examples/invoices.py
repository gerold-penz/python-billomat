#!/usr/bin/env python
# coding: utf-8

import pybillomat


# HTTP-Connection to Billomat
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
