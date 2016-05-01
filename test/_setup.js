// jquery magic.
var jsdom = require('jsdom');
var html = '<html><body></body></html>';
var doc = jsdom.jsdom(html);
var window = doc.defaultView;
global.$ = global.jQuery = require('jquery')(window);
