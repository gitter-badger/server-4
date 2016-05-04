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
global.ARGUX_BASE = '/';

describe('host', function() {
    // Unittests for poll_overview
    describe('poll_overview', function() {
        describe('_poll_overview_success', function() {
            it('callback should not throw exception', function() {
                host._poll_overview_success({});
            });
            it('check if #hosts is emptied before adding new children', function() {
                var hosts = $('#hosts');
                hosts.append('<tr><td>a</td></tr>');
                host._poll_overview_success({});
                assert(hosts.children().length == 0, '$("#hosts") should have 0 children, ' + hosts.children().length + ' found.');
            });
            it('check if hosts are added to #hosts', function() {
                var hosts = $('#hosts');
                hosts.empty();
                host._poll_overview_success({hosts: [{name: 'a', n_items: 0, active_alerts: 0}]});
                assert(hosts.children().length == 1, '$("#hosts") should have 1 children, ' + hosts.children().length + ' found.');
            });
        });
        describe('_poll_overview_complete', function() {
            it('callback should not throw exception', function() {
                host._poll_overview_complete();
            });
        });
        describe('_poll_overview_error', function() {
            it('callback should not throw exception', function() {
                host._poll_overview_error();
            });
        });
    });
    describe('create', function() {
        describe('_create_success', function() {
            it('callback should not throw exception', function() {
                host._create_success();
            });
        });
        describe('_create_error', function() {
            it('callback should not throw exception', function() {
                host._create_error();
            });
        });
    });
});
