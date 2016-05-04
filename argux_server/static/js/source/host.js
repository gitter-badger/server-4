host = {
    poll_overview: function () {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : host._poll_overview_success,
            error : host._poll_overview_error,
            complete : host._poll_overview_complete
        });
    },
    _poll_overview_success: function(json) {
        var total_active_alerts = 0;
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
            total_active_alerts+=value.active_alerts;
        });

        // Set the label on the alert tab
        if (total_active_alerts > 0) {
            $("#alert_count").text(total_active_alerts);
        } else {
            $("#alert_count").text('');
        }
    },
    _poll_overview_error: function(json) {
    },
    _poll_overview_complete: function(json) {
    },
    create: function(hostname) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host/'+hostname,
            success : host._create_success,
            error : host._create_error
        });
    },
    _create_error: function(json) {
    },
    _create_success: function(json) {
    }
};
