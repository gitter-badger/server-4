"""DNSMonitor module."""

import time
import platform

import re
import subprocess

import shutil
import os

from datetime import datetime

from .AbstractMonitor import AbstractMonitor

import transaction

def parse_dig(monitor, output):
    """Parse dig output.

    (python3.3)[stephan@hermes net-monitor]$ dig @server -t A example.com
    """
    ret_val = None
    answer = False
    for row in output.split('\n'):
        if answer == True:
            if row == '':
                break

            ret_val = row
        if row == ';; ANSWER SECTION:':
            answer = True
        print(row)

    return ret_val

DIG = {
    'FreeBSD': 'dig @{address} -t {_type} {domain}',
    'Darwin': 'dig @{address} -t {_type} {domain}',
    'SunOS': 'dig @{address} -t {_type} {domain}',
    'Linux': 'dig @{address} -t {_type} {domain}',
}

PARSE = {
    'FreeBSD': parse_dig,
    'Darwin': parse_dig,
    'SunOS': parse_dig,
    'Linux': parse_dig
}


class DNSMonitor(AbstractMonitor):

    """DNSMonitor class.

    Queries Monitor dao and schedules monitoring actions.
    """

    def run(self):
        """Run the DNSMonitor.

        Ignores the 'interval' option at the moment.
        DNS checks are executed at 300second intervals.
        """
        # Thread body.
        while True:

            cmd = shutil.which('dig', mode=os.X_OK)
            if cmd is not None:
                mons = self.dao\
                    .monitor_dao.get_all_monitors_for_type('DNS')
                for monitor in mons:
                    DNSMonitor.monitor_once(self.dao, monitor)
                DNSMonitor.monitor_once(self.dao, None)

            try:
                time.sleep(300)
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
        address = '8.8.8.8'
        #monitor.host_address.name
        _type = 'A'
        domain = 'example.com'

        dig_cmd = DIG[system_name].format(
            address=address,
            _type=_type,
            domain=domain)

        timestamp = datetime.now()

        try:
            output = subprocess.check_output(
                dig_cmd, shell=True, universal_newlines=True)

            val = PARSE[system_name](monitor, output)

            print(val)
        except:
            print('error')

        transaction.commit()

        return
