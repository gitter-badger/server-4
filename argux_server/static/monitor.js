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
              '"options":'+JSON.stringify(monitor.options)+
              '}',
        success: function() {
            $('#create-monitor-modal').modal('hide');
            return true;
        },
        error: function() {
            $('#trigger-form-alerts').append(
                '<div class="alert alert-danger alert-dismissible">'+
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                '<strong>Problem:</strong> Monitor could not be created.'+
                '</div>'
            );
        }
        
    });
}

function getAddresses(host) {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/host/"+
             host +
             "/addr",
        type: "GET",
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        success: function(json) {
            $('#monitor-address').empty();
            if(json.addresses.length == 0) {
                $('#monitor-address').append(
                    '<option disabled>No addresses</option>');
            } else {
                $.each(json.addresses, function(i, address) {
                    if (address.description != '') {
                        $('#monitor-address').append(
                            '<option value="'+address.name+'">'+
                            address.name+' ('+address.description+')'+
                            '</option>');
                    } else {
                        $('#monitor-address').append(
                            '<option value="'+address.name+'">'+
                            address.name +
                            '</option>');
                    }
                });
            }
            return true;
        },
        error: function() {
        }
    });
}

$(function() {
    monitor = {};

    if ((ARGUX_MONITOR_TYPE==="icmp") || (ARGUX_MONITOR_TYPE==="dns")) {
        var hostname = $('#monitor-host').val();
        getAddresses(hostname);
    }

    $('#monitor-host').on('change', function(e) {
        getAddresses(this.value);
    });

    $('#monitor-form').submit(function(event) {
        if ((ARGUX_MONITOR_TYPE==="icmp") || (ARGUX_MONITOR_TYPE==="dns")) {
            monitor = {
                'hostname': $('#monitor-host').val(),
                'address': $('#monitor-address').val(),
                'options' : {
                    'interval': $('#monitor-interval').val(),
                }
            };
        }

        event.preventDefault();
        createMonitor(monitor);
    });

    pollMonitors();
});
