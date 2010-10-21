try:
    import json
except ImportError:
    import simplejson as json
import api


def dumps(obj):
    try:
        return json.dumps(obj, separators=(',', ':'))
    except:
        raise api.SerializationException()

def loads(s):
    try:
        return json.loads(s)
    except:
        raise api.DeserializationException()


class Chunk(object):

    def __init__(self, data=None):
        self.data = data

    def to_network(self):
        return dumps(self.data)

    @classmethod
    def from_network(cls, s):
        return cls(loads(s))
