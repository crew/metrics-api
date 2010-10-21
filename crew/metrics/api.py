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
        :returns: On success,
            {
                "request": Request,
                "code": "success",
                "response": [{
                    field1: Number,
                    field2: Number,
                    namespace.field1: Number,
                    ...
                }, {
                    ...
                }]
            }
        On error,
            {
                "request": Request,
                "code": Number,
                "error": "Error message"
            }
        """

    def retrieve(self, namespace=None, apikey=None, start_time=None,
        end_time=None, interval=None, *fields, **attributes):
        """
        This is the call from the frontend to the backend.

        :param namespace: The namespace of the data.
        :param apikey: The secret key associated with the namespace.
        :param start_time: The starting datetime.
        :param end_time: The ending datetime.
        :param interval: The time interval.
        :param fields: The list of field names to retrieve.
        :param attributes: The list of attributes (key-value pairs) for
            filtering the dataset.
        :returns: A dictionary of this format.
            {
                "code": Number,
                (optional) "error": String,
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
