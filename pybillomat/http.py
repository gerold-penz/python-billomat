#!/usr/bin/env python
# coding: utf-8
"""
Connection
"""

import os
import urllib

if "APPENGINE_RUNTIME" in os.environ:
    # Google App Engine
    from google.appengine.api import urlfetch
    import zlib
    urllib3 = None
else:
    # Urllib3
    import urllib3
    urlfetch = None
import urlparse


class Connection(object):

    def __init__(
        self,
        billomat_id,
        billomat_api_key,
        billomat_app_id = None,
        billomat_app_secret = None,
        timeout_seconds = 600  # 10 Minutes
    ):

        self.timeout_seconds = timeout_seconds

        # Base URL
        self.url = "https://{billomat_id}.billomat.net/".format(
            billomat_id = billomat_id
        )

        # Headers
        self.headers = {
            "X-BillomatApiKey": billomat_api_key,
            "Content-Type": "application/xml",
        }
        if billomat_app_id:
            self.headers["X-AppId"] = billomat_app_id
        if billomat_app_secret:
            self.headers["X-AppSecret"] = billomat_app_secret

        # Bind Urlfetch for Google App Engine
        self.urlfetch = urlfetch

        # Initialize Urllib3-ConnectionPool
        if urllib3:
            scheme, host, port = urllib3.get_host(self.url)


            # ToDo: certifi einbauen und testen
            # https://urllib3.readthedocs.org/en/latest/security.html#using-certifi-with-urllib3
            # https://github.com/gerold-penz/python-billomat/issues/1


            self.conn = urllib3.HTTPSConnectionPool(
                host = host, port = port, timeout = self.timeout_seconds
            )

        else:
            self.conn = None


    def get(self, path):
        """
        GET-Request (allowes gzipped response)

        :returns: response
        """

        headers = self.headers.copy()
        headers["Accept-Encoding"] = "gzip"

        if self.conn:
            # Urllib3
            response = self.conn.request(method = "GET", url = path, headers = headers)
            return response
        else:
            # Google App Engine
            response = self.urlfetch.fetch(
                url = urllib.basejoin(self.url, path),
                method = "GET", headers = headers,
                deadline = self.timeout_seconds
            )
            response.status = response.status_code
            response.data = response.content

            # Decompress
            if "gzip" in response.headers.get("content-encoding", ""):
                response.data = zlib.decompressobj(16 + zlib.MAX_WBITS) \
                    .decompress(response.content)

            # Finished
            return response


    def _request_with_body(self, method, path, body):
        """
        POST/PUT/DELETE-Request (no gzipped response)

        :returns: response
        """

        headers = self.headers

        if self.conn:
            # Urllib3
            return self.conn.urlopen(
                method = method,
                url = path,
                body = body,
                headers = headers
            )
        else:
            # Google App Engine
            response = self.urlfetch.fetch(
                url = urllib.basejoin(self.url, path),
                payload = body,
                method = method,
                headers = headers,
                deadline = self.timeout_seconds
            )
            response.status = response.status_code
            response.data = response.content
            return response


    def post(self, path, body):
        """
        POST-Request (no gzipped response)

        :returns: response
        """

        return self._request_with_body(method = "POST", path = path, body = body)


    def put(self, path, body):
        """
        PUT-Request (no gzipped response)

        :returns: response
        """

        return self._request_with_body(method = "PUT", path = path, body = body)


    def delete(self, path, body = None):
        """
        DELETE-Request (no gzipped response)

        :returns: response
        """

        return self._request_with_body(method = "DELETE", path = path, body = body)


class Url(object):
    """
    Repräsentiert eine URL, wie sie im Onlineshop üblich ist.
    """

    __slots__ = [
        "scheme",
        "netloc",
        "path",
        "query",
        "fragment",
    ]


    def __init__(
        self,
        url = None,  # URL
        scheme = None,  # "http" oder "https"
        netloc = None,  # z.B. devshop.skischoolshop.com
        path = None,  # z.B. "/" oder "groupcourses"
        query = None,
        fragment = None
    ):
        """
        Info: ``<scheme>://<netloc>/<path>?<query>#<fragment>``

        :param scheme: "http" oder "https"
        :param netloc: z.B. "devshop.skischoolshop.com"
        :param path: z.B. "/" oder "groupcourses". Es kann aber auch ein
            itterierbares Objekt mit Strings übergeben werden. Der Pfad
            wird dann zusammengesetzt.
        :param query: Dictionary mit den Query-Key-Value-Paaren oder ein
            String. Ein String wird automatisch in ein Dictionary umgewandelt.
        :param fragment: Dictionary mit den Hash-Key-Value-Paaren oder ein
            String. Ein String wird automatisch in ein Dictionary umgewandelt.
        """

        # Falls die URL übergeben wurde...
        if url:
            (
                parsed_scheme,
                parsed_netloc,
                parsed_path,
                parsed_query,
                parsed_fragment
            ) = urlparse.urlsplit(url)
            if scheme is None:
                scheme = parsed_scheme
            if netloc is None:
                netloc = parsed_netloc
            if path is None:
                path = parsed_path
            if query is None:
                query = parsed_query
            if fragment is None:
                fragment = parsed_fragment

        # Scheme
        if isinstance(scheme, basestring):
            self.scheme = scheme.strip(":/")
        else:
            self.scheme = None

        # Netloc
        if isinstance(netloc, basestring):
            self.netloc = netloc.strip("/")
        else:
            self.netloc = None

        # Path
        if isinstance(path, basestring):
            self.path = path
        else:
            try:
                self.path = "/".join(path)
            except TypeError:
                self.path = None

        # Query
        if isinstance(query, basestring):
            if isinstance(query, unicode):
                query = query.encode("utf-8").strip(u"?&")
            for item_pair in query.split("&"):
                key, value = item_pair.split("=")
                self.query[key] = value
        else:
            self.query = query or {}

        # Fragment
        if isinstance(fragment, basestring):
            if isinstance(fragment, unicode):
                fragment = fragment.encode("utf-8").strip("?&")
            for item_pair in fragment.split("&"):
                key, value = item_pair.split("=")
                self.fragment[key] = value
        else:
            self.fragment = fragment or {}


    def __str__(self):
        """
        Gibt die URL als String zurück
        """

        if self.netloc:
            scheme = self.scheme or "http"
        else:
            scheme = None

        if isinstance(self.path, basestring):
            path = self.path
        else:
            try:
                path = "/".join(self.path) or "/"
            except TypeError:
                path = "/"

        if self.query:
            query = {}
            for key, value in self.query.items():
                if isinstance(key, unicode):
                    key = key.encode("utf-8")
                if isinstance(value, unicode):
                    value = value.encode("utf-8")
                query[key] = value
            query_str = urllib.urlencode(query)
        else:
            query_str = None

        if self.fragment:
            fragment = {}
            for key, value in self.fragment.items():
                if isinstance(key, unicode):
                    key = key.encode("utf-8")
                if isinstance(value, unicode):
                    value = value.encode("utf-8")
                fragment[key] = value
            fragment_str = urllib.urlencode(fragment)
        else:
            fragment_str = None

        return urlparse.urlunsplit((
            scheme,
            self.netloc,
            path,
            query_str,
            fragment_str
        ))


    __repr__ = __str__
