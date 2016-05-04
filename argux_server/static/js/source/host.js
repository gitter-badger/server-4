host = {
    poll_overview: function () {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : host.poll_overview_success,
            error : host.poll_overview_error,
            complete : host.poll_overview_complete
        });
    },
    poll_overview_success: function(json) {
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
    poll_overview_error: function(json) {
    },
    poll_overview_complete: function(json) {
    }
};
