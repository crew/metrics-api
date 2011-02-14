import unittest
from crew.metrics import wire


class TestWireHelpers(unittest.TestCase):

    def test_dumps(self):
        self.assertEquals(wire.dumps([]), "[]")
        self.assertEquals(wire.dumps(None), "null")
        self.assertEquals(wire.dumps(True), "true")
        self.assertEquals(wire.dumps(False), "false")
        self.assertEquals(wire.dumps(1), "1")
        self.assertEquals(wire.dumps("1"), '"1"')
        self.assertEquals(wire.dumps(1.2323), "1.2323")
        self.assertEquals(wire.dumps({}), "{}")

    def test_loads(self):
        self.assertEquals(wire.loads("[]"), [])
        self.assertEquals(wire.loads("null"), None)
        self.assertEquals(wire.loads("true"), True)
        self.assertEquals(wire.loads("false"), False)
        self.assertEquals(wire.loads("1"), 1)
        self.assertEquals(wire.loads("1.2323"), 1.2323)
        self.assertEquals(wire.loads("{}"), {})


class TestChunk(unittest.TestCase):

    def test_to_network(self):
        # TODO
        pass


if __name__ == '__main__':
    unittest.main()
