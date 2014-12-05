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


TESTFIRMA = 422909


# MITARBEITERNAME = 819
# OESTERREICH = 10031
#
# # client_tags_iterator = pybillomat.ClientTagsIterator(conn = conn)
# # client_tags_iterator.search(client_id = TESTFIRMA)
# #
# # for client_tag in client_tags_iterator:
# #     print client_tag
# #
#
# client_tag = pybillomat.ClientTag(conn = conn)
# client_tag.load(id = 1)

# article_properties_iterator = pybillomat.ArticlePropertiesIterator(conn = conn)
# article_properties_iterator.search()
#
# for property in article_properties_iterator:
#     print property
#

client = pybillomat.Client(conn = conn)
client.load(id = TESTFIRMA)
print client

client.edit(bank_account_number = u'999999')

client = pybillomat.Client(conn = conn)
client.load(id = TESTFIRMA)
print client
