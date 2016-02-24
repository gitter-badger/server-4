"""ICMPMonitor module."""

import time
import platform

import re
import subprocess

from .AbstractMonitor import AbstractMonitor

def parse_freebsd(monitor, output):
    """Parse FreeBSD PING output.

    (python3.3)[stephan@hermes net-monitor]$ ping -c 1 -t 5 -q localhost
    PING localhost (127.0.0.1): 56 data bytes

    --- localhost ping statistics ---
    1 packets transmitted, 1 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 0.079/0.079/0.079/0.000 ms
    """
    for row in output.split('\n'):
        m = re.search('^round-trip min/avg/max/stddev = (?P<min>[0-9]+(?:\.[0-9]+)?).*', row)
        if (m):
            print(m.group(1))

def parse_linux(monitor, output):
    """Parse Linux PING output.

    $ ping -c 1 -w 10 -q localhost
    PING localhost (127.0.0.1) 56(84) bytes of data.

    --- localhost ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.042/0.042/0.042/0.000 ms
    """
    for row in output.split('\n'):
        m = re.search('^rtt min/avg/max/mdev = (?P<min>[0-9]+(?:\.[0-9]+)?).*', row)
        if (m):
            print(m.group(1))

def parse_sunos(monitor, output):
    """Parse Solaris PING output.

    $ ping -s localhost 56 1
    PING localhost: 56 data bytes
    64 bytes from localhost (127.0.0.1): icmp_seq=0. time=0.300 ms

    ----localhost PING Statistics----
    1 packets transmitted, 1 packets received, 0% packet loss
    round-trip (ms)  min/avg/max/stddev = 0.300/0.300/0.300/NaN
    """
    for row in output.split('\n'):
        m = re.search('^round-trip \(ms\)  min/avg/max/stddev = (?P<min>[0-9]+(?:\.[0-9]+)?).*', row)
        if (m):
            print(m.group(1))

PING = {
    'FreeBSD': 'ping -c 1 -q {address}',
    'SunOS': 'ping -s {address} 56 1',
    'Linux': 'ping -c 1 -w 10 -q {address}'
}

PARSE = {
    'FreeBSD': parse_freebsd,
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
        system_name = platform.system()

        # Thread body.
        while True:

            mons = self.dao.monitor_dao.get_all_monitors_for_type('ICMP')
            for monitor in mons:
                address = monitor.host_address.name
                for o in monitor.options:
                    print(o.key)

                ping_cmd = PING[system_name].format(address=address)

                output = subprocess.check_output(ping_cmd, shell=True, universal_newlines=True)

                PARSE[system_name](monitor, output)

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
