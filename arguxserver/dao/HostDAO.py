from arguxserver.models import (
    DB_SESSION,
    Host
    )

class HostDAO(object):

    def get_host_by_name(self, name):
        h = DB_SESSION.query(Host).filter(Host.name == name).first()
        return h

    def create_host(self, name, description=""):
        h = Host(name=name, description=description)
        DB_SESSION.add(h)
        return h

    def get_all_hosts(self):
        h = DB_SESSION.query(Host)
        return h
