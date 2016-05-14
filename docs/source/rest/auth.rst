**************
Authentication
**************
First of all you need an authentication-token before you can do anything (ofcourse).

Get Authentication-Token
------------------------

CURL
^^^^
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
