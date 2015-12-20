/* globals Chart: false */
/* globals ARGUX_BASE: false */
/* globals ARGUX_HOST: false */
/* globals ARGUX_ITEM: false */
/* globals ARGUX_ITEM_ACTION: false */

/* globals TIMESPAN: false */

var chart_start_time = null;
var chart_end_time = 'now';

var config = {
    type: 'line',
    data: {
        datasets: [
            {
                label: ARGUX_ITEM,
                backgroundColor: "rgba(220,220,220,0.2)",
                data: [{x:'0',y:'1'}]
            }
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
                    //round: 'min'
                },
                scaleLabel: {
                    show: true,
                    labelString: 'Date/Time'
                }
            }, ],
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    suggestedMin: 0.0,
                    suggestedMax: 1.0,
                },
                scaleLabel: {
                    show: true,
                    labelString: ARGUX_ITEM
                }
            }]
        },
        elements: {
            line: {
                tension: 0.0
            }
        },
    }
};

var ctx;
var chart;

function pollItemValues(showValues, showAlerts, callback) {

    start_time = moment().subtract(30, 'minutes');

    if(chart_end_time === 'now') {
        now = moment();
        start_time = now.subtract(30, 'minutes');
        if(TIMESPAN==='30m') {
            start_time = now.subtract(30, 'minutes');
        }
        if(TIMESPAN==='12h') {
            start_time = now.subtract(12, 'hours');
        }
        if(TIMESPAN==='24h') {
            start_time = now.subtract(24, 'hours');
        }
        if(TIMESPAN==='7d') {
            start_time = now.subtract(7, 'days');
        }
    } else {
    }

    chart_start_time = start_time.format('YYYY-MM-DDTHH:mm:ss');

    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/host/"+
             ARGUX_HOST+
             "/item/"+
             ARGUX_ITEM+
             "/details?start="+
             chart_start_time+
             "&end="+
             chart_end_time+
             "&get_values="+
             showValues+
             "&get_alerts="+
             showAlerts,
        type: "GET",
        dataType: "json",
        success: function(json) {
            callback(json);
            if(json.active_alerts > 0) {
                $("#alert_count").text(json.active_alerts);
            } else {
                $("#alert_count").text('');
            }
        },
        complete: function(json) {
            setTimeout(
                pollItemValues,
                3000,
                showValues,
                showAlerts,
                callback);
        }
    });
}

function pollTriggers() {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/host/"+
             ARGUX_HOST+
             "/item/"+
             ARGUX_ITEM+
             "/trigger",
        type: "GET",
        dataType: "json",
        success: function(json) {

            $('#triggers').empty();

/*                    '<tr class="alert alert-warning"><td>' + */
/*                    '<span class="glyphicon glyphicon-exclamation-sign"></span> ' +*/
            $.each(json.triggers, function(i, trigger) {
                $('#triggers').append(
                    '<tr class=""><td>' +
                    '<span class="glyphicon glyphicon-none"></span> ' +
                    '<a href="#">' +
                    trigger.name +
                    '</a>' +
                    '</td><td>' +
                    trigger.rule +
                    '</td><td>' +
                    '0' +
                    '<a href="#" class="pull-right" data-toggle="tooltip" title="Remove Trigger">' +
                    '<span class="glyphicon glyphicon-remove"></span>' +
                    '</a>' +
                    '<a href="#" class="pull-right" data-toggle="tooltip" title="Edit Trigger">' +
                    '<span class="glyphicon glyphicon-edit"></span>' +
                    '</a>' +
                    '</td></tr>'
                );
            });
            setTimeout(pollTriggers, 3000);
        }
    });

}

function details_cb(json) {
    var datapoints = [];

    datapoints.push({
            x: json.start_time,
            });

    chart_start_time = json.start_time;

    if (json.values) {
        $.each(json.values, function(i, value) {
            datapoints.push({
                x: value.ts,
                y: value.value});
        });
    }

    datapoints.push({
            x: json.end_time,
            });


    config.data.datasets[0].data = datapoints;

    chart.update();
}

function alerts_cb(json) {

    $('#alerts').empty();

    if (json.alerts) {
        $.each(json.alerts, function(i, al) {
            if(al.severity === 'info') {
                icon = 'glyphicon-none';
            } else {
                icon = 'glyphicon-exclamation-sign';
            }
            $('#alerts').append(
                '<tr class=""><td>' +
                '<span class="glyphicon '+icon+'"></span> ' +
                '<a href="#">' +
                al.name +
                '</a>' +
                '</td><td>' +
                moment(al.start_time).fromNow(true) +
                '</td></tr>'
            );
        });
    }
}

$(function() {
    if (ARGUX_ITEM_ACTION==="details") {
        // Get the context of the canvas element we want to select
        ctx = document.getElementById("item-timechart").getContext("2d");
        chart = new Chart(ctx, config);
        pollItemValues(true, false, details_cb);
    }
    if (ARGUX_ITEM_ACTION==="alerts") {
        pollItemValues(false, true, alerts_cb);
    }
    if (ARGUX_ITEM_ACTION==="triggers") {
        pollTriggers();
    }
});
