SERVER=http://localhost:7000
ARGUX_BASE=/
REST_URI=rest/1.0
HOST_URI=host

HOST_NAME=localhost

ARGUX_USERNAME=admin
ARGUX_PASSWORD=admin

UNAMESTR=`uname`

if [[ "$UNAMESTR" == "Darwin" ]]; then
MKTEMP='mktemp -t argux'
else
MKTEMP='mktemp'
fi

HEADER_FILE=`$MKTEMP`
COOKIE_FILE=`$MKTEMP`

curl -X POST \
    -c $COOKIE_FILE \
    -D $HEADER_FILE \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{\"username\":\"$ARGUX_USERNAME\",\"password\":\"$ARGUX_PASSWORD\"}" \
    $SERVER/$REST_URI/login

CSRF_TOKEN=`cat $HEADER_FILE | grep -i X-CSRF-TOKEN | awk -F : '{ print $2 }'`

# Host
curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
       \"description\": \"Test adding new system\"
    }" \
    $SERVER/$REST_URI/$HOST_URI/ruby

# Host
curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    $SERVER/$REST_URI/$HOST_URI/webserver

# Host
curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
       \"description\": \"Test adding new system\",
       \"address\": [
            {
            \"address\": \"10.0.0.1\",
            \"description\": \"okay\"
            },
            {
            \"address\": \"10.0.0.2\"
            }
       ]
    }" \
    $SERVER/$REST_URI/$HOST_URI/perl

# Host
curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
       \"description\": \"Argux DEMO System\"
    }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME


# Host
curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
       \"description\": \"Argux DEMO System\"
       \"AAAAAAAAA\":\'A\'
    }" \
    $SERVER/$REST_URI/$HOST_URI/broken

