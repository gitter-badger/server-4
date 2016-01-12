
SERVER=http://localhost:6543
REST_URI=argux/rest/1.0
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
    $SERVER/login

CSRF_TOKEN=`cat $HEADER_FILE | grep -i X-CSRF-TOKEN | awk -F : '{ print $2 }'`

curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"message\":\"Lorem Ipsum\",
        \"subject\":\"TESTS\",
        \"host\": \"$HOST_NAME\"
        }" \
    $SERVER/$REST_URI/note

unlink $COOKIE_FILE
unlink $HEADER_FILE

exit 0
