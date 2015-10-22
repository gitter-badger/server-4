
SERVER=http://localhost:6543
REST_URI=argux/rest/1.0
HOST_URI=host

HOST_NAME=localhost


curl -X PUT $SERVER/$REST_URI/$HOST_URI/$HOST_NAME
curl -X PUT $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/cpu.load.avg\\\[1\\\]
curl -X PUT $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/cpu.load.avg\\\[5\\\]
curl -X PUT $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/cpu.load.avg\\\[15\\\]


# Store item with name and description
curl -X PUT \
     -H "Content-Type: application/json" \
     -d "{\"name\":\"System uptime\", \"description\":\"System Uptime\"}" \
     $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/sys.uptime
