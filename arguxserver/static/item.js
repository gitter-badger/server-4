/* globals Chart: false */
/* globals ARGUX_HOST: false */

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
                    format: 'MM/DD/YYYY HH:mm:SS',
                    //round: 'min'
                },
                scaleLabel: {
                    show: true,
                    labelString: 'Date'
                }
            }, ],
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                },
                scaleLabel: {
                    show: true,
                    labelString: 'value'
                }
            }]
        },
        elements: {
            line: {
                tension: 0.3
            }
        },
    }
};

// Get the context of the canvas element we want to select
var ctx = document.getElementById("myChart").getContext("2d");
var myNewChart = new Chart(ctx, config);

$(function() {
    function doPoll() {
        $.ajax({
            url: "/argux/rest/1.0/host/"+ARGUX_HOST+"/"+ARGUX_ITEM+"/values?query=a&show_date=false",
            type: "GET",
            dataType: "json",
            success: function(json) {

                var datapoints = [];

                $.each(json.values, function(i, value) {
                    datapoints.push({
                        x: value.ts,
                        y: value.value});
                });

                config.data.datasets[0].data = datapoints;

                myNewChart.update();

                setTimeout(doPoll, 3000);
            }
        });
    }
    doPoll();
});