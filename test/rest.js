require('../argux_server/static/js/source/rest.js');

var assert = require('chai').assert;

global.CSRF_TOKEN = 'a';

describe('rest', function() {
    describe('CallType', function() {
        it('CREATE should map to "POST"', function() {
            assert(rest.CallType.CREATE, "POST");
        });
        it('READ should map to "GET"', function() {
            assert(rest.CallType.READ, "GET");
        });
        it('UPDATE should map to "POST"', function() {
            assert(rest.CallType.UPDATE, "POST");
        });
        it('DELETE should map to "DELETE"', function() {
            assert(rest.CallType.DELETE, "DELETE");
        });
    });

    describe('#call', function() {
        it('should complete', function(done) {
            rest.call ({
                url: '/',
                type: rest.CallType.READ,
                complete:function() {done();}
            });
        });
    });
});
