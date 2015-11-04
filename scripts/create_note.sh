
SERVER=http://localhost:6543
REST_URI=argux/rest/1.0
HOST_URI=host

HOST_NAME=localhost

curl -X POST \
     -H "Content-Type: application/json" \
     -d "{
        \"message\":\"Lorem Ipsum\",
        \"subject\":\"TESTS\",
        \"host\": \"$HOST_NAME\"
        }" \
    $SERVER/$REST_URI/note

exit 0
