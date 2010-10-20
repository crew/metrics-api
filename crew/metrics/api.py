"""
The API "interface". Implementations should use subclasses to abstract out
the apikey and namespace handling.
"""


class API(object):
"""
The primitive metrics API object.
"""

    def store(self, namespace, apikey, timestamp, **kwargs):
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

    def retrieve(self, namespace, apikey, start_time, end_time, interval,
        *fields, **attributes):
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
