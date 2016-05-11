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
                '<a class="monitor-play-btn pause" ' +
                'data-hostname="' + monitor.host +'" ' +
                'data-address="' + monitor.address +'" ' +
                'data-type="' + ARGUX_MONITOR_TYPE +'" ' +
                '>' +
                '<span class="glyphicon glyphicon-pause"></span>' +
                '</a> ';
            } else {
                button =
                '<a href="#" class="monitor-play-btn" ' +
                'data-hostname="' + monitor.host +'" ' +
                'data-address="' + monitor.address +'" ' +
                'data-type="' + ARGUX_MONITOR_TYPE +'" ' +
                '>' +
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

        $('.monitor-play-btn').click(function() {
            var hostname = $(this).data('hostname'); 
            var address = $(this).data('address'); 
            var button = $(this);

            data = {
                "active": "true",
                "options" : {"interval": 60}
            };

            rest.call({
                url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+hostname+'/'+address,
                type : rest.CallType.UPDATE,
                data : data,
                success : function() {
                    button.addClass('pause');
                    button.children().removeClass('glyphicon-play');
                    button.children().addClass('glyphicon-pause');
                }
            });
        });

        $('.monitor-play-btn.pause').click(function() {
            var hostname = $(this).data('hostname'); 
            var address = $(this).data('address'); 
            var button = $(this);

            data = {
                "active": "false",
                "options" : {"interval": 60}
            };

            rest.call({
                url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+hostname+'/'+address,
                type : rest.CallType.UPDATE,
                data : data,
                success : function() {
                    button.removeClass('pause');
                    button.children().removeClass('glyphicon-pause');
                    button.children().addClass('glyphicon-play');
                }
            });
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
            url : ARGUX_BASE+'/rest/1.0/monitor/'+ARGUX_MONITOR_TYPE+'/'+hostname+'/'+address,
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
