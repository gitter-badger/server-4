"""SNMPMonitor module."""

import time
import platform

import re
import subprocess

from datetime import datetime

from .AbstractMonitor import AbstractMonitor

import transaction


class SNMPMonitor(AbstractMonitor):

    """SNMPMonitor class.

    Queries Monitor dao and schedules monitoring actions.
    """

    def run(self):
        """Run the SNMPMonitor.

        Ignores the 'interval' option at the moment.
        SNMP checks are executed at 60second intervals.
        """
        # Thread body.
        while True:

            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self.stop()

    @staticmethod
    def validate_options(options):
        if not 'interval' in options:
            raise KeyError

        return True

    @staticmethod
    def monitor_once(dao, monitor):
        """
        Monitor once.
        """
        system_name = platform.system()

        return
