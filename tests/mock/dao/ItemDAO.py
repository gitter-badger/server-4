
class Item:

    def __init__(self, host, key, name, category, itemtype):
        self.host = host
        self.key = key

def getItemsFromHost(host):
    return []

def getItemByHostKey(host, key):
    return None

def createItem(host, key, name, category, itemtype):
    i = Item(host, key, name, category, itemtype)
    return i
