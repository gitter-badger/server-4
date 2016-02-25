"""Monitors module."""

from .ICMPMonitor import ICMPMonitor

MONITORS = {}

def start_monitors(settings):
    MONITORS['ICMP'] = ICMPMonitor(settings)

    for monitor in MONITORS:
        MONITORS[monitor].start()
