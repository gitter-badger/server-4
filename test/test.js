require('./_setup.js');

var assert = require('chai').assert;
var r = require('../argux_server/static/js/source/rest.js');

global.CSRF_TOKEN = 'a';

describe('REST', function() {
    describe('CallType', function() {
        it('CREATE should map to "POST"', function() {
            assert(REST.CallType.CREATE, "POST");
        });
        it('READ should map to "GET"', function() {
            assert(REST.CallType.READ, "GET");
        });
        it('UPDATE should map to "POST"', function() {
            assert(REST.CallType.UPDATE, "POST");
        });
        it('DELETE should map to "DELETE"', function() {
            assert(REST.CallType.DELETE, "DELETE");
        });
    });

    describe('#call', function() {
        it('should complete', function(done) {
            REST.call ({
                url: '/',
                type: REST.CallType.READ,
                complete:function() {done();}
            });
        });
    });
});

