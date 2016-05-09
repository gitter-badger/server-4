
function update_complete_callback() {
    setTimeout(monitors.get_monitors, 60000, {'complete_callback' : update_complete_callback, 'type': ARGUX_MONITOR_TYPE});
}

$(function() {
    monitors.get_monitors({'complete_callback': update_complete_callback, 'type': ARGUX_MONITOR_TYPE});

    $('#monitor-form').submit(function(event) {
        monitors.create({
            'hostname': $('#monitor-host').val(),
            'address': $('#monitor-address').val(),
            'options': {
                'interval': $('#monitor-interval').val(),
            }
        })
    });

});
