require('../argux_server/static/js/source/rest.js');
require('../argux_server/static/js/source/host.js');

var assert = require('chai').assert;

global.CSRF_TOKEN = 'a';

describe('host', function() {
    describe('overview', function() {
        it('host-overview should create list', function() {
            assert(1, 1);
        });
    });
});
