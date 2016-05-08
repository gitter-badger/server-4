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
            args.type = rest.CallType.READ;
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
        if(args.data === undefined) {
            args.data = '';
        }

        $.ajax({
            url: args.url,
            type: args.type,
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            data: args.data,
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

var host_overview_chart_config = {
    type: 'doughnut',
    data: {
        datasets: [
            {
                data: [
                    0,
                    0,
                    0,
                    1 ],
                backgroundColor: [
                    "#419641",
                    "#f0ad4e",
                    "#c12e2a",
                    "#e0e0e0"]
            }
        ],
        labels: [
            "Okay",
            "Warning",
            "Critical",
            "Unknown"
            ]
    },
    options: {
        responsive: true,
        legend: {
            display: false,
        }
    }
};

host = {
    get_host_overview: function (complete_callback = function(){}) {
        rest.call({
            url : ARGUX_BASE+'/rest/1.0/host',
            success : host._get_host_overview_success,
            error : host._get_host_overview_error,
            complete : complete_callback
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

user = {

};
