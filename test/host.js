// jquery magic.
var jsdom = require('jsdom');
var html = '<html><body><table><tbody id="hosts"></tbody></body></html>';
var doc = jsdom.jsdom(html);
var window = doc.defaultView;
global.$ = global.jQuery = require('jquery')(window);

require('../argux_server/static/js/source/rest.js');
require('../argux_server/static/js/source/host.js');

var assert = require('chai').assert;

global.CSRF_TOKEN = 'a';

describe('host', function() {
    describe('poll_overview_complete', function() {
        it('check if hosts is emptied', function() {
            var a = $('#hosts');
            a.append('<tr><td>a</td></tr>');
            host.poll_overview_complete({});
            var size = Object.keys(a).length;
            assert(size, 0);
        });
        it('check if host is not empty', function() {
            var a = $('#hosts');
            a.append('<tr><td>a</td></tr>');
            host.poll_overview_complete({hosts: [{name: 'a', n_items: 0, active_alerts: 0}]});
            var size = Object.keys(a).length;
            assert(size, 2);
        });
    });
    describe('poll_overview_success', function() {
        it('just-a-test', function() {
            host.poll_overview_success('a');
        });
    });
    describe('poll_overview_error', function() {
        it('just-a-test', function() {
            host.poll_overview_error('a');
        });
    });
});
