# npm install uglify-js

./node_modules/uglify-js/bin/uglifyjs \
    ./argux_server/static/js/lib/debug/argux.js \
    -c -m \
    > ./argux_server/static/js/lib/argux.js


cp ./argux_server/static/js/source/overview.js \
   ./argux_server/static/js/debug/overview.js

./node_modules/uglify-js/bin/uglifyjs \
    ./argux_server/static/js/debug/overview.js \
    -c -m \
    > ./argux_server/static/js/overview.js
