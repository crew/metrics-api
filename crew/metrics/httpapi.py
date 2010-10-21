from wire import Chunk
from httplib import HTTPConnection
import api
import socket


class HttpAPI(object):
    """The primitive metrics API object."""

    def __init__(self, namespace=None, apikey=None, hostname=None, port=None,
            timeout=20):
        self.namespace = namespace
        self.apikey = apikey
        self.hostname = hostname
        self.port = port
        self.timeout = timeout

    def get_connection(self, timeout=None):
        timeout = timeout if timeout else self.timeout
        return HTTPConnection(self.hostname, self.port, timeout=timeout)

    def __update_request(self, request_dict, namespace, apikey):
        request_dict['namespace'] = namespace if namespace else self.namespace
        request_dict['apikey'] = apikey if apikey else self.apikey

    def __validate_store(self, timestamp):
        if not timestamp:
            raise api.ValidationError('Timestamp cannot be empty.')
        if not type(timestamp) == float:
            raise api.ValidationError('Timestamp has to be a float.')

    def store(self, namespace=None, apikey=None, timestamp=None, **kwargs):
        self.__validate_store(timestamp)
        kwargs['timestamp'] = timestamp
        self.__update_request(kwargs, namespace, apikey)
        c = Chunk(kwargs)
        try:
            conn = self.get_connection()
            req = conn.request('POST', '/store/', c.to_network())
            resp = conn.getresponse()
        except socket.timeout, e:
            raise api.TimeoutError(e)
        # Other exceptions are treated as an network error.
        except Exception, e:
            raise api.NetworkError(e)
        return Chunk.from_network(resp.read()).data

    def __validate_retrieve(self, start_time, end_time, interval):
        # TODO
        pass

    def retrieve(self, namespace=None, apikey=None, start_time=None,
            end_time=None, interval=None, *fields, **attributes):
        self.__validate_retrieve(start_time, end_time, interval)
        # TODO
