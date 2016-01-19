/* globals ARGUX_HOST: false */
/* globals ARGUX_HOST_ACTION: false */
/* globals ARGUX_BASE: false */
/* globals CSRF_TOKEN: false */

function pollHostDetails(callback, pollMetrics, pollAlerts) {
    if (pollMetrics || pollAlerts) {
        $.ajax({
            url: ARGUX_BASE+
                 "/rest/1.0/host/"+
                 ARGUX_HOST+
                 "?alerts="+pollAlerts+
                 "&items="+pollMetrics,
            type: "GET",
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            success: function(json) {
                if (callback) {
                    callback(json);
                }

                if(json.active_alerts > 0) {
                    $("#alert_count").text(json.active_alerts);
                } else {
                    $("#alert_count").text(''); }
            },
            comlete: function(json) {
                // Reschedule at complete, so the calls keep coming even
                // if the server is temporarily unavailable.
                setTimeout(
                    pollHostDetails,
                    3000,
                    callback,
                    pollMetrics,
                    pollAlerts);
            }
        });
    }
}

function pollNotes(callback) {
    $.ajax({
        url: ARGUX_BASE+"/rest/1.0/note?host="+ARGUX_HOST,
        type: "GET",
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        success: function(json) {

            callback(json);

            if(json.active_alerts > 0) {
                $("#alert_count").text(json.active_alerts);
            } else {
                $("#alert_count").text(''); }
        },
        comlete: function(json) {
            // Reschedule at complete, so the calls keep coming even
            // if the server is temporarily unavailable.
            setTimeout(
                pollNotes,
                3000,
                callback);
        }
    });
}

function notes_cb(json) {
    $('#items').empty();

    // Build the panel contents.
    $.each(json.notes, function(i, note) {

        // Note timestamp is in ISO format.
        var ts = new Date(note.timestamp);

        $('#items').append(
            '<div class="panel panel-default">' +
            '<div class="panel-heading">' +
            note.subject +
            '</div>' +
            '<div class="panel-body">' +
            '<p>' +
            note.message +
            '</p>' +
            '<div class="xs">' +
            ts.toLocaleString() +
            '</div>' +
            '</div>' +
            '</div>');
    });
}

function alerts_cb(json) {
    $('#alerts').empty();

    if (json.alerts) {
        $.each(json.alerts, function(i, al) {
            var severity = '';

            if(al.severity === 'info') {
                icon = 'glyphicon-none';
                severity = 'info';
            } else {
                if (al.severity === "crit") {
                    severity = "danger";
                }
                if (al.severity === "warn") {
                    severity = "warning";
                }
                icon = 'glyphicon-exclamation-sign';
            }

            if(al.acknowledgement === null) {
                ack = 'No (<a href="#">Acknowledge</a>)';
            } else {
                ack = 'Yes (<a href="#">Show Ack</a>)';
            }

            $('#alerts').append(
                '<tr class="'+severity+'"><td>' +
                '<span class="glyphicon '+icon+'"></span> ' +
                '<a href="/host/'+ARGUX_HOST+'/item/'+al.item.key+'">' +
                al.item.name +
                '</a>' +
                '</td><td>' +
                '<a href="/host/'+ARGUX_HOST+'/item/'+al.item.key+'/alerts">' +
                al.name +
                '</a>' +
                '</td><td>' +
                moment(al.start_time).fromNow(true) +
                '</td><td>' +
                ack +
                '</td></tr>'
            );
        });
    }
}

function metrics_cb(json) {
    var categories = {};
    var alerts     = {};
    var collapsed  = {};

    // Build the panel contents.
    $.each(json.items, function(i, item) {

        var category = 'global';
        var item_name = item.key;
        var item_value = 'unknown';
        var item_time = '-';

        // Pick a category
        if (item.category !== null) {
            category = item.category;
        }

        // If name exists, don't use the key.
        if (item.name !== null) {
            item_name = item.name;
        }

        //
        if (item.last_ts !== undefined) {
            item_time = item.last_ts;
        }

        if (item.last_val !== undefined) {
            item_value = item.last_val;
        }

        /* Initialise alerts to '' */
        if (alerts.hasOwnProperty(category) === false) {
            alerts[category] = '';
        }
        var item_base_url = 
            ARGUX_BASE +
            '/host/' +
            ARGUX_HOST +
            '/item/' +
            item.key;

        categories[category]+='<tr>' +
          '<td>' +
          '<a href="'+item_base_url+'">' +
          '<span ' +
          ' data-toggle="tooltip"' +
          ' title="'+item.key+'">' +
          item_name +
          '</span>' +
          '</a>' +
          '</td>' +
          '<td>' + item_value + '</td>' +
          '<td class="hidden-xs">' + item_time +'</td>' +
          '<td class="item-details">' +
          '<a href="'+item_base_url+'/bookmark" aria-label="Bookmark">' +
          '<span class="glyphicon glyphicon-bookmark" aria-hidden="true"></span>' +
          '</a>' +
          '</td>' +
          '</tr>';
    });

    // Determine if a panel was collapsed before the refresh.
    $('#items div.collapse').each(function(i, item) {
        var id = item.id.substring(12);
        collapsed[id] = $(this).hasClass('in');
    });

    // Remove all panels and build the page again.
    $('#items').empty();

    for (var key in categories) {
        if (categories.hasOwnProperty(key)) {
            $('#items').append(
                '<div class="panel panel-default">' +
                '<div class="panel-heading metric-category">' +
                '<a data-toggle="collapse" data-target="#table-items-'+key+'">' +
                key +
                ' <span class="badge">'+alerts[key]+'</span>' +
                '</a>' +
                '</div>' +
                '<div class="collapse in" id="table-items-'+key+'">' +
                '<table class="table table-striped table-condensed">' +
                '<thead>' +
                '<tr>' + 
                '<th>Name</th>' +
                '<th class="col-xs-2">Value</th>' +
                '<th class="col-sm-3 hidden-xs">Timestamp</th>' +
                '<th class="col-xs-2 col-sm-1"></th>' +
                '</tr>' +
                '</thead>' +
                '<tbody>' +
                '<tbody id="items-'+key+'">' +
                '</tbody>' +
                '</table>' +
                '</div>' +
                '</div>');

            // Collapse panels that were collapsed before the refresh.
            if (collapsed[key] === false) {
                $('#table-items-'+key).removeClass('in');
            }

            // Add the panel-content.
            $('#items-'+key).append(
                categories[key]
                );
        }
    }
}

$(function() {
    if (ARGUX_HOST_ACTION==='notes') {
        $('#notes-form').submit(function(event) {

            event.preventDefault();

            var subject = $('#note-subject').val();
            var message = $('#note-body').val();

            if (( subject !== "") &&
                ( message !== "")) {
                // Use JSON.stringify to properly escape the message and subject
                // for use in a JSON message envelope
                $.ajax({
                    url:  ARGUX_BASE+'/rest/1.0/note',
                    type: 'POST',
                    headers: { 'X-CSRF-Token': CSRF_TOKEN },
                    dataType: 'json',
                    data: '{'+
                          '"host": "'+ARGUX_HOST+'",' +
                          '"message": '+JSON.stringify(message)+',' +
                          '"subject": '+JSON.stringify(subject)+
                          '}',
                    error: function(json) {
                        $('#alerts').empty();
                        $('#alerts').append(
                            '<div class="alert alert-danger alert-dismissible">'+
                            '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                            '<strong>Problem:</strong> Creating new Note failed.'+
                            '</div>');
                    },
                    complete: function(json) {
                        $('#new-note-modal').modal('hide');
                    }
                });
            }
        });
        pollNotes(notes_cb);
    }

    if (ARGUX_HOST_ACTION==='metrics') {
        pollHostDetails(metrics_cb, true, false);
    }

    if (ARGUX_HOST_ACTION==='alerts') {
        pollHostDetails(alerts_cb, false, true);
    }
});

// Show/hide details below host header.
$("#host_detail_btn").click(function(e) {
    var span = $('#host_detail_btn > span');
    $('#host_detail').toggleClass('hidden');
    if ($('#host_detail').is('.hidden')) {
        span.addClass('glyphicon-chevron-up');
        span.removeClass('glyphicon-chevron-down');
    } else {
        span.addClass('glyphicon-chevron-down');
        span.removeClass('glyphicon-chevron-up');
    }
});
