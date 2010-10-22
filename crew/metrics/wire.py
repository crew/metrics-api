try:
    import json
except ImportError:
    import simplejson as json
import api


def dumps(obj):
    """
    :param obj: The python object to be serialized to JSON.
    :returns: The string of the python object.
    :rtype: str
    >>> class X(object):
    ...     def __str__(self):
    ...         return 'X'
    >>> dumps({1: 2, 3: 4})
    '{"1":2,"3":4}'
    >>> dumps(X())
    Traceback (most recent call last):
        ...
    SerializationException: X
    """
    try:
        return json.dumps(obj, separators=(',', ':'))
    except:
        raise api.SerializationException(obj)


def loads(s):
    """
    :param s: The string to be deserialized from JSON into a python object.
    :returns: A python object based on the given JSON string.
    >>> loads('{"one": 2, "three": 4}') == {'one': 2, 'three': 4}
    True
    >>> loads('{')
    Traceback (most recent call last):
        ...
    DeserializationException: {
    """
    try:
        return json.loads(s)
    except:
        raise api.DeserializationException(s)


class Chunk(object):
    """
    A wrapper around JSON.
    >>> c = Chunk()
    >>> c.data = {}
    >>> c.data
    {}
    """

    def __init__(self, data=None):
        """
        >>> c = Chunk()
        """
        self.data = data

    def to_network(self):
        """
        >>> c = Chunk({"hello": "world"})
        >>> c.to_network()
        '{"hello":"world"}'
        """
        return dumps(self.data)

    @classmethod
    def from_network(cls, s):
        """
        >>> c = Chunk.from_network('{"hello":"world"}')
        >>> c.data == {"hello": "world"}
        True
        """
        return cls(loads(s))
