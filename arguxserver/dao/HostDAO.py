"""Data Access Object class for handling Hosts."""

from arguxserver.models import (
    DB_SESSION,
    Host
)


def get_host_by_name(name):
    """Return host-object based on name."""
    host = DB_SESSION.query(Host).filter(Host.name == name).first()
    return host


def create_host(name, description=""):
    """Create host."""
    host = Host(name=name, description=description)

    DB_SESSION.add(host)

    return host


def get_all_hosts():
    """Return all hosts."""
    hosts = DB_SESSION.query(Host)
    if hosts is None:
        return []

    return hosts
