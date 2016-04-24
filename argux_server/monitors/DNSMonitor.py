"""DNSMonitor module."""

import time
import platform

import re
import subprocess

import shutil
import os

from datetime import datetime

from .AbstractMonitor import AbstractMonitor

from argux_server.rest.client import (
    RESTClient,
    monitor_manager,
)

def parse_dig(monitor, output):
    """Parse dig output.

    (python3.3)[stephan@hermes net-monitor]$ dig @server +noall +answer -t A example.com
    """
    ret_val = []
    answer = False
    for row in output.split('\n'):
            m = re.search(
                '^(?P<name>[^ \t]+)[ \t]+'+
                '(?:(?P<ttl>[0-9]+)[ \t]+)?'+
                '(?P<in>[^ \t]+)[ \t]+'+
                '(?P<type>[^ \t]+)[ \t]+'+
                '(?:(?P<prio>[0-9]+)[ \t]+)?'+
                '(?P<value>[^ ]+)', row)
            if (m):
                ret_val.append({
                    'name': m.group('name'),
                    'ttl': m.group('ttl'),
                    'ttl': m.group('in'),
                    'type': m.group('type'),
                    'value': m.group('value'),
                    'prio': m.group('prio')
                    })

    return ret_val

DIG = 'dig @{address} +noall +answer -t {_type} {domain}'

PARSE = parse_dig

class DNSMonitor(AbstractMonitor):

    """DNSMonitor class.

    Queries Monitor schedules monitoring actions.
    """

    def run(self):
        """Run the DNSMonitor.

        Ignores the 'interval' option at the moment.
        DNS checks are executed at 300second intervals.
        """
        # Thread body.
        while True:
            cmd = shutil.which('dig', mode=os.X_OK)

            try:
                mons = monitor_manager.get_monitors(self.client, 'dns')
                for mon in mons:
                    try:
                        DNSMonitor.monitor_once(self.client, mon)
                    except Exception as e:
                        print(str(e))
            except Exception as e:
                print(str(e))

            try:
                time.sleep(10)
            except KeyboardInterrupt:
                self.stop()

        self.session.close()

    @staticmethod
    def validate_options(options):
        if not 'interval' in options:
            raise ValueError

        return True

    @staticmethod
    def monitor_once(client, monitor):
        """
        Monitor once.
        """
        system_name = platform.system()

        items = {}
        val = None
        _type = None
        domain = None

        domains = monitor_manager.get_dns_domains(
            client,
            monitor['host'],
            monitor['address'])

        for domain in domains:
            if domain['record_a']:
                DNSMonitor.check_dns(client, monitor, 'A', domain['domain'])
            if domain['record_aaaa']:
                DNSMonitor.check_dns(client, monitor, 'AAAA', domain['domain'])
            if domain['record_mx']:
                DNSMonitor.check_dns(client, monitor, 'MX', domain['domain'])

        return

    def check_dns(client, monitor, _type, domain):
        timestamp = datetime.now()
        values = []

        address = monitor['address']
        host = monitor['host']

        dig_cmd = DIG.format(
            address=address,
            _type=_type,
            domain=domain)

        try:
            output = subprocess.check_output(
                dig_cmd, shell=True, universal_newlines=True)
            values = PARSE(monitor, output)
        except Exception as e:
            print('error '+str(e))

        item_key = 'dns.ttl[type='+_type+',domain='+domain+']'
        if True:
            params = {
                'name': 'DNS TTL for '+domain+' '+_type+' record.',
                'type': 'int',
                'category': 'Network',
                'unit': 'Seconds',
                'description': 'DNS record information',
            }

            client.create_item(
                host,
                item_key,
                params)

        for a in values:
            print(a['ttl'])
            print(a['value'])

        #print('------')
        #for a in sorted(val, key=lambda value: a['value']):
        #    print(a)
