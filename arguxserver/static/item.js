/* globals Chart: false */
/* globals ARGUX_BASE: false */
/* globals ARGUX_HOST: false */
/* globals ARGUX_ITEM: false */
/* globals ARGUX_ITEM_ACTION: false */

/* globals TIMESPAN_START: false */
/* globals TIMESPAN_END: false */

var config = {
    type: 'line',
    data: {
        datasets: [
            {
                label: ARGUX_ITEM,
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(110,110,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
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
                    format: 'DD/MM/YYYY HH:mm:SS',
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


function pollItemValues() {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/host/"+
             ARGUX_HOST+
             "/item/"+
             ARGUX_ITEM+
             "/values?start="+TIMESPAN_START+"&end="+TIMESPAN_END,
        type: "GET",
        dataType: "json",
        success: function(json) {

            var datapoints = [];

            start = moment().subtract(30, 'minute');
            end   = moment();

            datapoints.push({
                    x: start.format('DD/MM/YYYY HH:mm:ss'),
                    });

            if (json.values.length > 0) {
                $.each(json.values, function(i, value) {
                    datapoints.push({
                        x: value.ts,
                        y: value.value});
                });
            }

            datapoints.push({
                    x: end.format('DD/MM/YYYY HH:mm:ss'),
                    });


            config.data.datasets[0].data = datapoints;

            chart.update();

            setTimeout(pollItemValues, 3000);
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

$(function() {
    if (ARGUX_ITEM_ACTION==="details") {
        // Get the context of the canvas element we want to select
        ctx = document.getElementById("item-timechart").getContext("2d");
        chart = new Chart(ctx, config);
        pollItemValues();
    }
    if (ARGUX_ITEM_ACTION==="triggers") {
        pollTriggers();
    }
});
