
SERVER=http://localhost:6543
REST_URI=argux/rest/1.0
HOST_URI=host

HOST_NAME=localhost


curl -X POST $SERVER/$REST_URI/$HOST_URI/$HOST_NAME
curl -X POST $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/cpu.load.avg\\\[1\\\]
curl -X POST $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/cpu.load.avg\\\[5\\\]
curl -X POST $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/cpu.load.avg\\\[15\\\]


# Store item with name and description
curl -X POST \
     -H "Content-Type: application/json" \
     -d "{\"name\":\"System uptime\", \"description\":\"System Uptime\"}" \
     $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/sys.uptime

# Store item with name and description
curl -X POST \
     -H "Content-Type: application/json" \
     -d "{\"name\":\"Incoming network traffic on interface eth0\", \"description\":\"Network traffic measured in bytes/s\", \"category\": \"net\"}" \
     $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/net.if\\\[eth0\\\].in

# Store item with name and description
curl -X POST \
     -H "Content-Type: application/json" \
     -d "{\"name\":\"Incoming network traffic on interface eth1\", \"description\":\"Network traffic measured in bytes/s\", \"category\": \"net\"}" \
     $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/net.if\\\[eth1\\\].in
