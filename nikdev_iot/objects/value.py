# -*- coding: utf-8 -*-


class Value:

    field_id = None
    """ 
    The field id to store the value to.
    
    :type: str
    """

    value = None
    """
    The actual value that is sent to the server.

    :type: str|int|float|bool
    """

    timestamp = None
    """
    (optional) Timestamp that stores the timestamp when the value was set. 
    Only for read, will not sent on upload or converted with to_object function.
    
    :type: int
    """

    def __init__(self, field_id=None, value=None, timestamp=None):
        """
        Initializes a value object, either for reading or storing on the IoT Server.

        :param str                  field_id:   The field id or json object to serialize from.
        :param str|int|float|bool   value:      (optional) The value of the field.
        :param int                  timestamp:  (optional) The timestamp of the set value.
        """
        self.field_id = field_id
        self.value = value
        self.timestamp = timestamp

    @classmethod
    def from_json_downstream(cls, json_data):
        """
        Initializes a value object from json_data that's been fetched for downstream data.

        :param json_data: JSON-data that initialize the object.
        :type json_data: dict
        """
        # Fetch the key and extract the values
        field_id = json_data.keys()[0]
        values = json_data[field_id]
        # Calls the main constructor and provides extracted values.
        return cls(
            field_id=field_id,
            value=values.get('value'),
            timestamp=values.get('timestamp'),
        )

    @classmethod
    def from_json_upstream(cls, json_data):
        """
        Initializes a value object from json_data that's been fetched for upstream data.

        :param json_data: JSON-data that initialize the object.
        :type json_data: dict
        """
        # Fetch the key and extract the value
        field_id = json_data.keys()[0]
        value = json_data[field_id]
        # Calls the main constructor and provides extracted values.
        return cls(
            field_id=field_id,
            value=value
        )

    def to_object_downstream(self):
        """
        Converts the object to an object that represents what the server responds with.

        :return:    A represented dict to represents what the server sends.
        :rtype:     dict[str, str|int|float|bool, int|None]
        """
        return {
            self.field_id: {
                'value': self.value,
                'timestamp': self.timestamp if self.timestamp is not None else None
            }
        }

    def to_object_upstream(self):
        """
        Converts the object to an object that can be sent to the server.

        :return:    A represented dict to store on server.
        :rtype:     dict[str, str|int|float|bool]
        """
        return {
            self.field_id: self.value
        }

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.field_id == other.field_id
        else:
            return False
