from arguxserver.models import (
    DBSession,
    Host
    )

class HostDAO(object):

    def getHostByName(self, name):
        h = DBSession.query(Host).filter(Host.name == name).first()
        return h

    def createHost(self, name, description=""):
        h = Host(name=name, description=description)
        DBSession.add(h)
        return h

    def getAllHosts(self):
        h = DBSession.query(Host)
        return h
