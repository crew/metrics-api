import unittest
from crew.metrics import httpapi

API = httpapi.HttpAPI
HTTPConnection = httpapi.HTTPConnection
HTTPSConnection = httpapi.HTTPSConnection

# TODO mock httpclient and test sending request


class TestHttpAPI(unittest.TestCase):

    def test_init(self):
        API()
        a = API(url='https://example.com')
        self.assertEquals(a.ssl, True)
        self.assertEquals(a.port, 443)
        self.assertEquals(a.hostname, 'example.com')
        b = API(url='http://example.net:2020')
        self.assertEquals(b.ssl, False)
        self.assertEquals(b.port, 2020)
        self.assertEquals(b.hostname, 'example.net')

    def test_get_connection(self):
        a = API(url='http://example.com')
        self.assertEquals(a.get_connection().__class__, HTTPConnection)
        b = API(url='https://example.com')
        self.assertEquals(b.get_connection().__class__, HTTPSConnection)


if __name__ == '__main__':
    unittest.main()
