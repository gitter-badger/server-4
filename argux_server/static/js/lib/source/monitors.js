monitors = {
    get_monitors: function (args) {
        if (args.complete_callback === undefined) {
            args.complete_callback = function(){};
        }
        rest.call({
            url : ARGUX_BASE + '/rest/1.0/monitor/' + args.type,
            success : monitors._get_monitors_success,
            complete: args.complete_callback
        });
    },
    _get_monitors_success: function(json) {
        $('#monitors').empty();
        $.each(json.monitors, function(i, monitor) { options = '';
            $.each(monitor.options, function(key, value) {
                options+= '<li><span style="font-weight: bold">'+key+':</span> '+value+'</li>';
            });
            if (monitor.active) {
                button = 
                '<a href="#">' +
                '<span class="glyphicon glyphicon-pause"></span>' +
                '</a> ';
            } else {
                button =
                '<a href="#">' +
                '<span class="glyphicon glyphicon-play"></span>' +
                '</a> ';
            }
            $('#monitors').append(
                '<tr class=""><td>' +
                button +
                '<a href="'+ARGUX_BASE+'/monitor/'+ARGUX_MONITOR_TYPE+'/'+monitor.host+'/'+monitor.address+'/edit">' +
                monitor.host +
                ' (' + monitor.address + ')' +
                '</a>' +
                '</td><td>' +
                '<ul>' +
                options + 
                '</ul>' +
                '</td></tr>'
            );
        });
    }
};
