
class Host:
    name = "A"

    def __init__(self, name, description="a"):
        self.name = "localhost"


def getHostByName(name):
    return Host("name")

def createHost(name, description=""):
    h = Host(name, description)
    return h

def getAllHosts():
    h = Host('a')
    return [h]
