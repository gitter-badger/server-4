
SERVER=http://localhost:6543
REST_URI=rest/1.0
HOST_URI=host

HOST_NAME=localhost

for i in {1..59}
do

cmd="date -v-"$i"M +%FT%TZ"

TS=`$cmd`
RND=$(((RANDOM%100)))

VAL=0.$RND

curl -X POST \
     -H "Content-Type: application/json" \
     -d "{
        \"value\":\"$VAL\",
        \"timestamp\":\"$TS\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[5\\\]/values

done
