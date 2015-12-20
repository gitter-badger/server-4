/* globals ARGUX_HOST: false */
/* globals ARGUX_HOST_ACTION: false */
/* globals ARGUX_BASE: false */

function pollNotes() {
    $.ajax({
        url: ARGUX_BASE+"/rest/1.0/note?host="+ARGUX_HOST,
        type: "GET",
        dataType: "json",
        success: function(json) {

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
            setTimeout(pollNotes, 5000);
        }
    });
}

function pollAlerts() {
    $.ajax({
        url: ARGUX_BASE+"/rest/1.0/host/"+ARGUX_HOST+"?alerts=true",
        type: "GET",
        dataType: "json",
        success: function(json) {

            $('#alerts').empty();

            if (json.alerts) {
                $.each(json.alerts, function(i, al) {
                    if(al.severity === 'info') {
                        icon = 'glyphicon-none';
                    } else {
                        icon = 'glyphicon-exclamation-sign';
                    }

                    if(al.acknowledgement === null) {
                        ack = 'No (<a href="#">Acknowledge</a>)';
                    } else {
                        ack = 'Yes (<a href="#">Show Ack</a>)';
                    }

                    $('#alerts').append(
                        '<tr class=""><td>' +
                        '<span class="glyphicon '+icon+'"></span> ' +
                        '<a href="#">' +
                        al.item +
                        '</a>' +
                        '</td><td>' +
                        '<a href="#">' +
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
            if(json.active_alerts > 0) {
                $("#alert_count").text(json.active_alerts);
            } else {
                $("#alert_count").text('');
            }
        }
    });
}

function pollMetrics() {
    $.ajax({
        url: ARGUX_BASE+"/rest/1.0/host/"+ARGUX_HOST+"?items=true",
        type: "GET",
        dataType: "json",
        success: function(json) {

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
                if (item.category !== null) { category = item.category;
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
                  item_name +
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
                        '<div class="panel-heading">' +
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

            setTimeout(pollMetrics, 5000);
        }
    });

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
                    type: 'POST',
                    url:  ARGUX_BASE+'/rest/1.0/note',
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

        pollNotes();
    }

    if (ARGUX_HOST_ACTION==='metrics') {
        pollMetrics();
    }

    if (ARGUX_HOST_ACTION==='alerts') {
        pollAlerts();
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
