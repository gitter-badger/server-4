# npm install uglify-js

./node_modules/uglify-js/bin/uglifyjs \
    ./argux_server/static/js/lib/debug/argux.js \
    -c -m \
    > ./argux_server/static/js/lib/argux.js

for b in `ls ./argux_server/static/js/source/*.js`
do
    a=`basename $b`

    cp ./argux_server/static/js/source/$a \
       ./argux_server/static/js/debug/$a

    ./node_modules/uglify-js/bin/uglifyjs \
        ./argux_server/static/js/debug/$a \
        -c -m \
        > ./argux_server/static/js/$a
done
