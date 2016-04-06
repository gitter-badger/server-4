"""ICMPMonitor module."""

import time
import platform

import re
import subprocess

from datetime import datetime

from .AbstractMonitor import AbstractMonitor

import transaction

def parse_freebsd(monitor, output):
    """Parse FreeBSD PING output.

    (python3.3)[stephan@hermes net-monitor]$ ping -c 1 -t 5 -q localhost
    PING localhost (127.0.0.1): 56 data bytes

    --- localhost ping statistics ---
    1 packets transmitted, 1 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 0.079/0.079/0.079/0.000 ms
    """
    ret_val = None
    for row in output.split('\n'):
        m = re.search('^round-trip min/avg/max/stddev = (?P<min>[0-9]+(?:\.[0-9]+)?).*', row)
        if (m):
            ret_val = str(float(m.group(1))/1000)
    return ret_val

def parse_linux(monitor, output):
    """Parse Linux PING output.

    $ ping -c 1 -w 10 -q localhost
    PING localhost (127.0.0.1) 56(84) bytes of data.

    --- localhost ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.042/0.042/0.042/0.000 ms
    """
    ret_val = None
    for row in output.split('\n'):
        m = re.search('^rtt min/avg/max/mdev = (?P<min>[0-9]+(?:\.[0-9]+)?).*', row)
        if (m):
            ret_val = str(float(m.group(1))/1000)
    return ret_val

def parse_sunos(monitor, output):
    """Parse Solaris PING output.

    $ ping -s localhost 56 1
    PING localhost: 56 data bytes
    64 bytes from localhost (127.0.0.1): icmp_seq=0. time=0.300 ms

    ----localhost PING Statistics----
    1 packets transmitted, 1 packets received, 0% packet loss
    round-trip (ms)  min/avg/max/stddev = 0.300/0.300/0.300/NaN
    """
    ret_val = None
    for row in output.split('\n'):
        m = re.search('^round-trip \(ms\)  min/avg/max/stddev = (?P<min>[0-9]+(?:\.[0-9]+)?).*', row)
        if (m):
            ret_val = str(float(m.group(1))/1000)
    return ret_val

PING = {
    'FreeBSD': 'ping -c 1 -q {address}',
    'Darwin': 'ping -c 1 -q {address}',
    'SunOS': 'ping -s {address} 56 1',
    'Linux': 'ping -c 1 -w 10 -q {address}'
}

PARSE = {
    'FreeBSD': parse_freebsd,
    'Darwin': parse_freebsd,
    'SunOS': parse_sunos,
    'Linux': parse_linux
}


class ICMPMonitor(AbstractMonitor):

    """ICMPMonitor class.

    Queries Monitor dao and schedules monitoring actions.
    """

    def run(self):
        """Run the ICMPMonitor.

        Ignores the 'interval' option at the moment.
        ICMP checks are executed at 60second intervals.
        """
        # Thread body.
        while True:

            mons = self.dao.monitor_dao.get_all_monitors_for_type('ICMP')
            for monitor in mons:
                ICMPMonitor.monitor_once(self.dao, monitor)

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

        item_key = 'icmpping[env=local,addr='+address+',responsetime]'
        items[item_key] = dao.item_dao\
            .get_item_by_host_key(
                monitor.host_address.host,
                item_key
            )
        if items[item_key] is None:
            item_type = dao.item_dao\
                .get_itemtype_by_name(name='float')

            items[item_key] = dao.item_dao\
                .create_item(
                    {
                        'host': monitor.host_address.host,
                        'key': item_key,
                        'name': 'Ping response-time from '+address+' to (local)',
                        'itemtype': item_type,
                        'category': 'Network',
                        'unit': 'Seconds'
                    }
                )

        item_key = 'icmpping[env=local,addr='+address+',alive]'
        items[item_key] = dao.item_dao\
            .get_item_by_host_key(
                monitor.host_address.host,
                item_key
            )
        if items[item_key] is None:
            item_type = dao.item_dao\
                .get_itemtype_by_name(name='boolean')

            items[item_key] = dao.item_dao\
                .create_item(
                    {
                        'host': monitor.host_address.host,
                        'key': item_key,
                        'name': 'Ping response from '+address+' to (local)',
                        'itemtype': item_type,
                        'category': 'Network'
                    }
                )

        ping_cmd = PING[system_name].format(address=address)

        timestamp = datetime.now()

        try:
            output = subprocess.check_output(ping_cmd, shell=True, universal_newlines=True)

            val = PARSE[system_name](monitor, output)

            if val is not None:
                dao.item_dao.push_value(
                    items['icmpping[env=local,addr='+address+',responsetime]'],
                    timestamp,
                    val)

        except subprocess.CalledProcessError:
            val = None

        if val is not None:
            dao.item_dao.push_value(
                items['icmpping[env=local,addr='+address+',alive]'],
                timestamp,
                True)
        else:
            dao.item_dao.push_value(
                items['icmpping[env=local,addr='+address+',alive]'],
                timestamp,
                False)

        transaction.commit()

        return
