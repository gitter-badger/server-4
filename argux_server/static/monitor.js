/* globals ARGUX_BASE: false */
/* globals ARGUX_HOST: false */
/* globals CSRF_TOKEN: false */

function pollMonitors() {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/monitor/"+
             ARGUX_MONITOR_TYPE,
        type: "GET",
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        success: function(json) {
            $('#monitors').empty();
            $.each(json.monitors, function(i, monitor) {
                options = '';
                $.each(monitor.options, function(key, value) {
                    options+= '<li><span style="font-weight: bold">'+key+':</span> '+value+'</li>';
                });
                $('#monitors').append(
                    '<tr class=""><td>' +
                    '<span class="glyphicon glyphicon-down-arrow"></span>' +
                    monitor.host +
                    '</td><td>' +
                    monitor.address +
                    '</td><td>' +
                    '<ul>' +
                    options + 
                    '</ul>' +
                    '</td><td>' +
                    '&nbsp;' +
                    '</td></tr>'
                );
            });
        },
        complete: function() {
            setTimeout(
                pollMonitors,
                3000);
        }
    });
}

function validateMonitor(monitor) {

}

function createMonitor(monitor) {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/monitor/"+
             ARGUX_MONITOR_TYPE+
             "/"+
             monitor.hostname+
             "/"+
             monitor.address,
        type: "POST",
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        data: '{'+
              '"options":'+
                  '{'+
                  '"interval":'+JSON.stringify(monitor.interval)+
                  '}'+
              '}',
        success: function() {
            $('#create-monitor-modal').modal('hide');
            return true;
        },
        error: function() {
            $('#trigger-form-alerts').append(
                '<div class="alert alert-danger alert-dismissible">'+
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                '<strong>Problem:</strong> Trigger rule could not be created.'+
                '</div>'
            );
        }
        
    });

}

$(function() {
    monitor = {};

    if (ARGUX_MONITOR_TYPE==="icmp") {
        monitor = {
            'hostname': $('#monitor-host').val(),
            'address': $('#monitor-address').val(),
            'interval': $('#monitor-interval').val(),
        };
    }

    $('#monitor-form').submit(function(event) {
        event.preventDefault();
        createMonitor(monitor);
    });

    pollMonitors();
});
