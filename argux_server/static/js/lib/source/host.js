host = {
    get_host_overview: function(args) {
        if (args.complete_callback === undefined) {
            args.complete_callback = function(){};
        }
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : host._get_host_overview_success,
            error : host._get_host_overview_error,
            complete : args.complete_callback
        });
    },
    _get_host_overview_success: function(json) {
        var total_active_alerts = 0;
        var graph_data = [0,0,0,0];

        $('#hosts').empty();
        $.each(json.hosts, function(i, value) {
            $('#hosts').append(
                '<tr><td>' +
                '<a href="'+ARGUX_BASE+'/host/' + value.name + '">' +
                value.name +
                '</a></td><td>' +
                '<a href="'+ARGUX_BASE+'/host/' + value.name + '/metrics">' +
                value.n_items +
                '</a></td><td>' +
                '<a href="'+ARGUX_BASE+'/host/' + value.name + '/alerts">' +
                value.active_alerts+
                '</a></td></tr>'
            );

            if (value.severity === 'crit') {
                graph_data[2] += 1;
            } else if (value.severity === 'warn') {
                graph_data[1] += 1;
            } else if (value.severity === 'info') {
                graph_data[3] += 1;
            } else {
                graph_data[0] += 1;
            }

            total_active_alerts+=value.active_alerts;
        });

        host_overview_chart_config.data.datasets[0].data = graph_data;

        // Set the label on the alert tab
        if (total_active_alerts > 0) {
            $("#alert_count").text(total_active_alerts);
        } else {
            $("#alert_count").text('');
        }
    },
    _get_host_overview_error: function(json) {
    },
    create: function(args) {
        if (args.hostname === undefined) {
            throw "Hostname argument missing";
        }
        if (args.description === undefined) {
            description = '';
        } else {
            description = args.description;
        }
        if (args.addresses === undefined) {
            addresses = []
        } else {
            addresses = args.addresses;
        }

        data = {
            "description": description,
            "address": addresses
        };

        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+hostname,
            data : data,
            success : host._create_success,
            error : host._create_error
        });
    },
    _create_error: function(json) {
    },
    _create_success: function(json) {
    }
};
