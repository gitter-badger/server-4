
from .ItemNameDAO import ItemName

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
