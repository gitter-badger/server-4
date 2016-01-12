SERVER=http://localhost:6543
ARGUX_BASE=/
REST_URI=rest/1.0
HOST_URI=host

HOST_NAME=localhost

HEADER_FILE=`mktemp`
COOKIE_FILE=`mktemp`

curl -X POST \
    -c $COOKIE_FILE \
    -D $HEADER_FILE \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{\"username\":\"s\",\"password\":\"s\"}" \
    $SERVER/$REST_URI/login

CSRF_TOKEN=`cat $HEADER_FILE | grep -i X-CSRF-TOKEN | awk -F : '{ print $2 }'`

curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"name\":\"CPU Load > 5\",
        \"rule\":\"last() > 5\",
        \"description\":\"CPU Load > 5\",
        \"severity\":\"warn\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[15\\\]/trigger

exit 0
