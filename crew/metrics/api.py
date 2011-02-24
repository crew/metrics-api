"""
The API "interface". Implementations should use subclasses to abstract out
the apikey and namespace handling.
"""


class API(object):
    """The primitive metrics API object."""

    def store(self, namespace=None, apikey=None, timestamp=None, **kwargs):
        """
        This is the call from the "aggregator" to the backend.

        :param namespace: The namespace of the data.
        :param apikey: The secret key associated with the namespace.
        :param timestamp: The event datetime.
        :param kwargs: The key-value mapping of the data (includes both
            fields and attributes).
        :returns: A dictionary of this format.

            .. code-block:: python

                {
                    "code": Number,
                    "error": String, # (optional)
                }

        """

    def retrieve(self, namespace=None, apikey=None, start_time=None,
            end_time=None, interval=None, fields=None, attributes=None):
        """
        This is the call from the frontend to the backend.

        :param namespace: The namespace of the data.
        :param apikey: The secret key associated with the namespace.
        :param start_time: The starting datetime.
        :param end_time: The ending datetime.
        :param interval: The time interval.
        :param fields: The list of field names to retrieve.
        :param attributes: The key-value pairs of attributes to values for
            filtering the dataset.
        :returns: On success,

            .. code-block:: python

                {
                    "request": Request,
                    "code": "success",
                    "response": [
                        {
                            field1: Number,
                            field2: Number,
                            namespace.field1: Number,
                            ...
                        }, {
                            ...
                        }
                    ]
                }

            On error,

            .. code-block:: python

                {
                    "request": Request,
                    "code": Number,
                    "error": "Error message"
                }
        """

    def retrieve_last(self, namespace=None, apikey=None, fields=None,
            attributes=None, limit=1):
        """
        This is the call from the frontend to the backend for the most
        recent data.

        :param namespace: The namespace of the data.
        :param apikey: The secret key associated with the namespace.
        :param fields: The list of field names to retrieve.
        :param attributes: The key-value pairs of attributes to values for
            filtering the dataset.
        :param limit: The number of objects to return, by default this is 1.
        :returns: On success,

            .. code-block:: python

                {
                    "request": Request,
                    "code": "success",
                    "response": [
                        {
                            field1: Number,
                            field2: Number,
                            namespace.field1: Number,
                            ...
                        }, {
                            ...
                        }
                    ]
                }

            On error,

            .. code-block:: python

                {
                    "request": Request,
                    "code": Number,
                    "error": "Error message"
                }
        """


class CrewMetricsException(Exception):

    def __init__(self, wrapped=None, *args, **kwargs):
        msg = None if not wrapped else str(wrapped)
        Exception.__init__(self, msg, *args, **kwargs)
        self.wrapped = wrapped


class SerializationException(CrewMetricsException):
    """Thrown when the request cannot be serialized."""


class DeserializationException(CrewMetricsException):
    """Thrown when the response cannot be deserialized."""


class ValidationError(CrewMetricsException):
    """Argument validation."""


class TimeoutError(CrewMetricsException):
    """The request timed out."""


class NetworkError(CrewMetricsException):
    """Connection/network error."""
