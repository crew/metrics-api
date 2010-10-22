from wire import Chunk
from httplib import HTTPConnection
import api
import validation
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
        validation.check_float(timestamp, 'timestamp')

    def store(self, namespace=None, apikey=None, timestamp=None, **kwargs):
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
            end_time=None, interval=None, fields=None, attributes=None):
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
        except socket.timeout, e:
            raise api.TimeoutError(e)
        # Other exceptions are treated as an network error.
        except Exception, e:
            raise api.NetworkError(e)
        return Chunk.from_network(resp.read()).data
