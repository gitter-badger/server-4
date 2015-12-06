from datetime import datetime, timedelta

from .ItemNameDAO import ItemName

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
_items['localhost'] = [Item('localhost', 'cpu.load.avg[1]', ItemName('CPU Load Average'), None, 'int')]

def getItemsFromHost(host):
    if (host.name == 'localhost'):
        return _items['localhost']
    return []

def getItemByHostKey(host, key):
    return None

def createItem(host, key, name, category, itemtype):
    i = Item(host, key, name, category, itemtype)
    return i

def pushValue(item, timestamp, value):
    return

def getLastValue(item):
    return MockValue(42, datetime.now(), 1)

def getValues(item):
    return []
