from arguxserver.models import (
    DB_SESSION,
    Host
    )

def get_host_by_name(name):
    h = DB_SESSION.query(Host).filter(Host.name == name).first()
    return h

def create_host(name, description=""):
    h = Host(name=name, description=description)
    DB_SESSION.add(h)
    return h

def get_all_hosts():
    h = DB_SESSION.query(Host)
    return h
