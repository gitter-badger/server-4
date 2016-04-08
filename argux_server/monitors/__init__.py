"""Monitors module."""

from .ICMPMonitor import ICMPMonitor
from .DNSMonitor import DNSMonitor

MONITORS = {}

def start_monitors(settings):
    MONITORS['ICMP'] = ICMPMonitor(settings)
    MONITORS['DNS'] = DNSMonitor(settings)

    for monitor in MONITORS:
        MONITORS[monitor].start()
