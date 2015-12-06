from datetime import datetime, timedelta

class MockValue():
    def __init__(self, value, timestamp, item_id):
        self.value = value
        self.timestamp = timestamp


# Map
__push_value_class = {
    "int" : MockValue,
    "float" : MockValue
}


