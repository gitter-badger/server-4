from arguxserver.models import (
    DB_SESSION,
    Host
    )

class HostDAO(object):

    def getHostByName(self, name):
        h = DB_SESSION.query(Host).filter(Host.name == name).first()
        return h

    def createHost(self, name, description=""):
        h = Host(name=name, description=description)
        DB_SESSION.add(h)
        return h

    def getAllHosts(self):
        h = DB_SESSION.query(Host)
        return h
