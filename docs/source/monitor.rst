========
Monitors
========

ICMP Monitor
------------
The ICMP Monitor executes the `ping` command and performs an
ICMP echo request to a specified host-address. The results of
this command are stored in items associated with this host.

.. image:: images/icmp_monitor_overview.png

Add a new ICMP Monitor
^^^^^^^^^^^^^^^^^^^^^^
.. image:: images/icmp_monitor_add.png

Delete an ICMP Monitor
^^^^^^^^^^^^^^^^^^^^^^
.. image:: images/icmp_monitor_delete.png

DNS Monitor
-----------
The DNS Monitor can be used to monitor a DNS server and guard
it's responses. It executes the `dig` command to retrieve specific
information about a DNS record and stores those results with
associated items.

SNMP Monitor
------------
.. NOTE::
The SNMP Monitor is not yet implemented, any suggestions are welcome.

JMX Monitor
-----------
.. NOTE::
The JMX Monitor is not yet implemented, it requires a java proxy that
translates to the binary JMX protocol.
