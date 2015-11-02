
SERVER=http://localhost:6543
REST_URI=argux/rest/1.0
HOST_URI=host

HOST_NAME=localhost


# Host
curl -X POST \
    -H "Content-Type: application/json" \
    -d "{
       \"description\": \"Argux DEMO System\"
    }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME

curl -X POST \
     -H "Content-Type: application/json" \
     -d "{
        \"name\":\"CPU Load (1 minute average)\",
        \"description\":\"1 Minute average of CPU load\",
        \"type\":\"float\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[1\\\]

curl -X POST \
     -H "Content-Type: application/json" \
     -d "{
        \"name\":\"CPU Load (5 minute average)\",
        \"description\":\"5 Minute average of CPU load\",
        \"type\":\"float\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[5\\\]

curl -X POST \
     -H "Content-Type: application/json" \
     -d "{
        \"name\":\"CPU Load (15 minute average)\",
        \"description\":\"15 Minute average of CPU load\",
        \"type\":\"float\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[15\\\]


# Store item with name and description
curl -X POST \
     -H "Content-Type: application/json" \
     -d "{
        \"name\":\"System uptime\",
        \"description\":\"System Uptime\",
        \"type\":\"int\"
        }" \
     $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/sys.uptime

curl -X POST \
     -H "Content-Type: application/json" \
     -d "{
        \"value\":\"0.12\",
        \"timestamp\":\"2015-12-31T22:11:10Z\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[1\\\]/values
