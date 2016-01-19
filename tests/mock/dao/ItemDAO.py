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

class Item:

    def __init__(self, host, key, name, category, itemtype):
        self.host = host
        self.key = key
        self.name = name
        self.category = category
        self.itemtype = itemtype

_items = {}
_items['localhost'] = [Item('localhost', 'cpu.load.avg[1]', 'CPU Load Average', None, 'int')]

def get_items_from_host(host):
    if (host.name == 'localhost'):
        return _items['localhost']
    return []

def get_item_by_host_key(host, key):
    return None

def create_item(host, key, name, category, itemtype):
    i = Item(host, key, name, category, itemtype)
    return i

def push_value(item, timestamp, value):
    return

def get_last_value(item):
    return MockValue(42, datetime.now(), 1)

def get_values(item):
    return []

def get_active_alert_count(item):
    return 0

def get_item_count_from_host(item):
    return 0
