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

            mons = self.dao.monitor_dao.get_all_monitors_for_type('SNMP')
            for monitor in mons:
                SNMPMonitor.monitor_once(self.dao, monitor)

            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self.stop()

        self.session.close()

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

        items = {}
        val = None
        address = monitor.host_address.name


        transaction.commit()

        return
