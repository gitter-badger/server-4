"""Monitors module."""

from .ICMPMonitor import ICMPMonitor

MONITORS = {
    'ICMP': ICMPMonitor()
}

def start_monitors():
    for monitor in MONITORS:
        MONITORS[monitor].start()
