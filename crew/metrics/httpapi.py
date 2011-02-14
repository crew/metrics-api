import socket
from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
from .wire import Chunk
from . import api
from . import validation


class HttpAPI(object):
    """
    The primitive metrics API object.

    Since the namespace and the apikey would most likely be reused, you can
    create the object with the default namespace and apikey so you do not
    have to pass them in every time.
    """

    def __init__(self, namespace=None, apikey=None, hostname=None, port=None,
            timeout=20, ssl=False, url=None):
        """
        :param namespace: The namespace.
        :param apikey: The apikey.
        :param hostname: The hostname to connect.
        :param port: The port number.
        :param timeout: The timeout for requests in seconds.
        :param ssl: True if the connection should be SSL.
        :param url: The url to connect. This overrides hostname, port, and
            ssl.

        >>> x = HttpAPI(url='https://www.example.net/')
        >>> x.ssl
        True
        >>> x.port
        443
        >>> x.hostname
        'www.example.net'
        >>> x = HttpAPI(url='https://www.example.net:2020')
        >>> x.ssl
        True
        >>> x.port
        2020
        >>> x.hostname
        'www.example.net'
        """
        self.namespace = namespace
        self.apikey = apikey
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.ssl = ssl
        if url:
            o = urlparse(url)
            self.ssl = o.scheme == 'https'
            self.port = 443 if self.ssl else 80
            if o.port is not None:
                self.port = o.port
            self.hostname = o.netloc.split(':')[0]

    def get_connection(self, timeout=None):
        """
        Creates a connection object. Used internally.

        :param timeout: The timeout in seconds.

        >>> x = HttpAPI(url='https://www.example.net')
        >>> x.get_connection().__class__ == HTTPSConnection
        True
        >>> x = HttpAPI(url='http://www.example.net')
        >>> x.get_connection().__class__ == HTTPConnection
        True
        """
        timeout = timeout if timeout else self.timeout
        if self.ssl:
            return HTTPSConnection(self.hostname, self.port, timeout=timeout)
        return HTTPConnection(self.hostname, self.port, timeout=timeout)

    def __update_request(self, request_dict, namespace, apikey):
        """
        (internal)
        Replaces the request_dict with the default namespace and apikey if
        they are not provided.

        :param request_dict: The request dictionary.
        :param namespace: The namespace.
        :param apikey: The API key.
        """
        request_dict['namespace'] = namespace if namespace else self.namespace
        request_dict['apikey'] = apikey if apikey else self.apikey

    def __validate_store(self, timestamp):
        validation.check_float(timestamp, 'timestamp')

    def store(self, namespace=None, apikey=None, timestamp=None, **kwargs):
        """
        Store a metric.

        :param namespace: The namespace.
        :param apikey: The API key.
        :param timestamp: (required) The timestamp.
        :param kwargs: The data.
        """
        self.__validate_store(timestamp)
        kwargs['timestamp'] = timestamp
        self.__update_request(kwargs, namespace, apikey)
        chunk = Chunk(kwargs)
        return self._send_request('/store/', Chunk(kwargs))

    def __validate_retrieve(self, start_time, end_time, interval, fields):
        validation.check_float(start_time, 'start_time')
        validation.check_float(end_time, 'end_time')
        validation.check_int(interval, 'interval')
        validation.check_list(fields, str, 'fields')

    def retrieve(self, namespace=None, apikey=None, start_time=None,
            end_time=None, interval=None, fields=None, attributes={}):
        """
        Retrieve data.

        :param namespace: The namespace.
        :param apikey: The API key.
        :param start_time: (required) The start datetime as a UNIX time.
        :param end_time: (required) The end datetime as a UNIX time.
        :param interval: (required) (not implemented) The time interval.
        :param fields: The list of fields to fetch. The timestamp is always
            included.
        :param attributes: The attribute mapping in which to filter.
        """
        fields = fields if fields else []
        request = dict(attributes)
        self.__update_request(request, namespace, apikey)
        self.__validate_retrieve(start_time, end_time, interval, fields)
        request['start_time'] = start_time
        request['end_time'] = end_time
        request['interval'] = interval
        request['fields'] = fields
        return self._send_request('/retrieve/', Chunk(request))

    def _send_request(self, url, chunk, method='POST'):
        try:
            conn = self.get_connection()
            req = conn.request(method, url, chunk.to_network())
            resp = conn.getresponse()
        except socket.timeout as e:
            raise api.TimeoutError(e)
        # Other exceptions are treated as an network error.
        except Exception as e:
            raise api.NetworkError(e)
        return Chunk.from_network(resp.read()).data
