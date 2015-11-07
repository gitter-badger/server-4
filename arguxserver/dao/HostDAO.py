from arguxserver.models import (
    DBSession,
    Host
    )


def getHostByName(name):
    h = DBSession.query(Host).filter(Host.name == name).first()
    return h

def createHost(name, description=None):
    h = Host(name=name, description=description)
    DBSession.add(h)
    return h

def getAllHosts():
    h = DBSession.query(Host)
    return h
    
