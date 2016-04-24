========
REST API
========

**************
Authentication
**************

CURL
----
The following script is an example using CURL::

   #!/bin/bash
   HEADER_FILE=`mktemp`
   COOKIE_FILE=`mktemp`

   curl -X POST \
        -c $COOKIE_FILE \
        -D $HEADER_FILE \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "{\"username\":\"jdoe\",\"password\":\"password\"}" \
        http://localhost/rest/1.0/login

   CSRF_TOKEN=`cat $HEADER_FILE |\
      grep -i X-CSRF-TOKEN |\
      awk -F : '{ print $2 }'`

The Session Cookie and Cross-Site-Request-Forgery token must be
preserved for any following requests.

*****
Hosts
*****
Section describing Host API.

CREATE Host
===========
Create a host

CURL
~~~~
Create a host using the following command::

   #!/bin/bash
   curl -X POST \
        -b $COOKIE_FILE \
        -H "Content-Type: application/json" \
        -H "X-CSRF-Token: $CSRF_TOKEN" \
        -d "{
           \"description\": \"Argux DEMO System\"
        }" \
        http://localhost/rest/1.0/host/HOSTNAME

Read Host
=========
todo...

Update Host
===========
todo...

Delete Host
===========
Delete a host

CURL
~~~~
Delete a host using the following command::

   #!/bin/bash
   curl -X DELETE \
        -b $COOKIE_FILE \
        -H "Content-Type: application/json" \
        -H "X-CSRF-Token: $CSRF_TOKEN" \
        http://localhost/rest/1.0/host/HOSTNAME
