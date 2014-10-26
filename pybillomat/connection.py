#!/usr/bin/env python
# coding: utf-8
"""
Connection
"""

import urllib3


class Connection(urllib3.HTTPSConnectionPool):

    def __init__(
        self,
        billomat_id,
        billomat_api_key,
        billomat_app_id = None,
        billomat_app_secret = None,
    ):

        # Base URL
        url = "https://{billomat_id}.billomat.net/".format(billomat_id = billomat_id)

        # Headers
        headers = {
            "X-BillomatApiKey": billomat_api_key,
            "Accept-Encoding": "gzip",
            "Content-Type": "application/xml",
        }
        if billomat_app_id:
            headers["X-AppId"] = billomat_app_id
        if billomat_app_secret:
            headers["X-AppSecret"] = billomat_app_secret


        # Initialize ConnectionPool
        scheme, host, port = urllib3.get_host(url)
        urllib3.HTTPSConnectionPool.__init__(
            self,
            host = host,
            port = port,
            headers = headers
        )




