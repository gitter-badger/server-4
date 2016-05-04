var argux = {
    VERSION: "0.0.1"
};

rest = {
    CallType : {
        CREATE : "POST",
        READ : "GET",
        UPDATE : "POST",
        DELETE: "DELETE"
    },
    call: function (args) {
        if(args.type === undefined) {
            args.type = REST.CallType.READ;
        }
        if(args.success === undefined) {
            args.success = function(json){};
        }
        if(args.error === undefined) {
            args.error = function(json){};
        }
        if(args.complete === undefined) {
            args.complete = function(){};
        }

        $.ajax({
            url: args.url,
            type: args.type,
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            success: function(json) {
                args.success(json);
            },
            error: function(json) {
                args.error(json);
            },
            complete: function() {
                args.complete();
            }
        });
    }
};



var history_chart_config = {
    type: 'line',
    data: {
        datasets: [
        ]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                type: "time",
                display: true,
                time: {
                    format: 'YYYY-MM-DDTHH:mm:SS',
                    displayFormats: {
                        'millisecond': 'SSS [ms]',
                        'second': 'HH:mm:ss', // 23:20:01
                        'minute': 'MM/DD HH:mm', // 23:20:01
                        'hour': 'YY/MM/DD HH:00', // 2015/12/22 23:00
                        'day': 'YY/MM/DD', // 2015/12/22
                        'month': 'MMM YYYY', // Sept 2015
                        'quarter': '[Q]Q - YYYY', // Q3 - 2015
                        'year': 'YYYY', // 2015
                    },
                },
                scaleLabel: {
                    show: true,
                    labelString: 'Date/Time'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    suggestedMin: 0.0,
                    suggestedMax: 1.0,
                    callback: function(value) {
                        if(unit.symbol){
                            return ''+Math.round(value*10)/10+' '+item_unit_prefix+unit.symbol;
                        } else {
                            return ''+Math.round(value*10)/10;
                        }
                    }
                },
                scaleLabel: {
                    show: true,
                }
            }]
        },
        elements: {
            line: {
                tension: 0.0
            },
            point: {
                radius: 1
            }
        },
    }
};

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
