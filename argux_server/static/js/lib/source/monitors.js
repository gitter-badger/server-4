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
                '<a class="monitor-pause-btn" ' +
                'data-hostname="' + monitor.host +'" ' +
                'data-address="' + monitor.address +'" ' +
                'data-type="' + ARGUX_MONITOR_TYPE +'" ' +
                '>' +
                '<span class="glyphicon glyphicon-pause"></span>' +
                '</a> ';
            } else {
                button =
                '<a href="#" class="argux-monitor-play-btn">' +
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

        $('.monitor-pause-btn').click(function() {
            alert('> '+ $(this).data('hostname')+ ' > ' + $(this).data('address') + ' > ' + ARGUX_MONITOR_TYPE);
        });

    },
    create: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.address === undefined) {
            throw "address argument missing";
        }
        if (args.options === undefined) {
            args.options = {}
        }

        data = {
            "options": args.options
        };

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/monitor/'+args.hostname+'/'+args.address,
            type : rest.CallType.CREATE,
            data : data,
            success : monitors._create_success,
            error : monitors._create_error
        });
    },
    _create_error: function(json) {
    },
    _create_success: function(json) {
    }
};
