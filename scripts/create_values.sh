
SERVER=http://localhost:7000
REST_URI=rest/1.0
HOST_URI=host

HOST_NAME=localhost

ARGUX_USERNAME=admin
ARGUX_PASSWORD=admin

HEADER_FILE=`mktemp`
COOKIE_FILE=`mktemp`

curl -X POST \
    -c $COOKIE_FILE \
    -D $HEADER_FILE \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{\"username\":\"$ARGUX_USERNAME\",\"password\":\"$ARGUX_PASSWORD\"}" \
    $SERVER/$REST_URI/login

CSRF_TOKEN=`cat $HEADER_FILE | grep -i X-CSRF-TOKEN | awk -F : '{ print $2 }'`

for i in {1..5}
do

cmd="date -v-"$i"M +%FT%TZ"

TS=`$cmd`
RND=$(((RANDOM%100)))

VAL=5.$RND

curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"value\":\"$VAL\",
        \"timestamp\":\"$TS\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[15\\\]/values
done

unlink $COOKIE_FILE
unlink $HEADER_FILE
