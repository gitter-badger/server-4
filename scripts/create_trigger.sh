SERVER=http://localhost:6543
ARGUX_BASE=/
REST_URI=rest/1.0
HOST_URI=host

HOST_NAME=localhost

curl -X POST \
     -v \
     -H "Content-Type: application/json" \
     -d "{
        \"name\":\"CPU Load > 5\",
        \"rule\":\"last() > 5\",
        \"description\":\"CPU Load > 5\",
        \"severity\":\"warn\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[15\\\]/trigger

exit 0
