"""DNSMonitor module."""

import time
import platform

import re
import subprocess

import shutil
import os

import sqlalchemy

from datetime import datetime

from .AbstractMonitor import AbstractMonitor

import transaction

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
    def monitor_once(dao, monitor):
        """
        Monitor once.
        """
        system_name = platform.system()

        items = {}
        val = None
        _type = None
        domain = None

        for domain in monitor.domains:
            print(domain.domain)
            if domain.record_a:
                DNSMonitor.check_dns(monitor, dao, 'A', domain.domain)
            if domain.record_aaaa:
                DNSMonitor.check_dns(monitor, dao, 'AAAA', domain.domain)
            if domain.record_mx:
                DNSMonitor.check_dns(monitor, dao, 'MX', domain.domain)


        transaction.commit()

        return

    def check_dns(monitor, dao, _type, domain):
        timestamp = datetime.now()
        values = []

        address = monitor.host_address.name

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
        ttl_item = dao.item_dao\
            .get_item_by_host_key(
                monitor.host_address.host,
                item_key
            )

        if ttl_item is None:
            print("NO TTL ITEM FOUND");
            item_type = dao.item_dao\
                .get_itemtype_by_name(name='int')

            ttl_item = dao.item_dao\
                .create_item(
                    {
                        'host': monitor.host_address.host,
                        'key': item_key,
                        'name': 'DNS '+_type+' record for '+domain,
                        'itemtype': item_type,
                        'category': 'Network',
                    }
                )

        for a in values:
            print(a['value'])

        #print('------')
        #for a in sorted(val, key=lambda value: a['value']):
        #    print(a)
