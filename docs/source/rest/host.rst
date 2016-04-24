Hosts
=====
Section describing Host API.

CREATE Host
-----------
Create a host

CURL
^^^^
Create a host using the following command::

   curl -X POST \
        -b $COOKIE_FILE \
        -H "Content-Type: application/json" \
        -H "X-CSRF-Token: $CSRF_TOKEN" \
        -d "{
           \"description\": \"Argux DEMO System\"
        }" \
        http://localhost/rest/1.0/host/HOSTNAME

Read Host
---------
todo...

Update Host
-----------
todo...

Delete Host
-----------
Delete a host

CURL
^^^^
Delete a host using the following command::

   curl -X DELETE \
        -b $COOKIE_FILE \
        -H "Content-Type: application/json" \
        -H "X-CSRF-Token: $CSRF_TOKEN" \
        http://localhost/rest/1.0/host/HOSTNAME
