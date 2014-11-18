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

client = pybillomat.Client.create(
    conn = conn,
    archived = None,
    number_pre = None,
    number = None,
    number_length = None,
    name = "TESTKUNDE 4",
    street = None,
    zip = "6406",
    city = u"Oberhofen im Inntal",
    state = None,
    country_code = "AT",
    first_name = u"Gerold ÖÄÜ",
    last_name = None,
    salutation = None,
    phone = None,
    fax = None,
    mobile = None,
    email = None,
    www = None,
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

print client
