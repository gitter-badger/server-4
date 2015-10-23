from arguxserver.models import (
    DBSession,
    Host
    )


def getHostByName(name):
    h = DBSession.query(Host).filter(Host.name == name).first()
    return h

def createHost(name):
    h = Host(name=name)
    DBSession.add(h)
    return h
