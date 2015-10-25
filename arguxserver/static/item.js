/* globals Chart: false */
/* globals ARGUX_HOST: false */

Chart.defaults.global.responsive = true;

var data = {
    labels: [],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(110,110,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: []
        }
    ]
};

// Get the context of the canvas element we want to select
var ctx = document.getElementById("myChart").getContext("2d");
var myNewChart = null;

$(function() {
    function doPoll() {
        $.ajax({
            url: "/argux/rest/1.0/host/"+ARGUX_HOST+"/"+ARGUX_ITEM+"/values?query=a&show_date=false",
            type: "GET",
            dataType: "json",
            success: function(json) {

                var labels = [];
                var datapoints = [];

                $.each(json.values, function(i, value) {
                    labels.push(value.ts);
                    datapoints.push(value.value);
                });

                data.datasets[0].data = datapoints;
                data.labels = labels;

                if (myNewChart !== null) {
                    myNewChart.destroy();
                }

                myNewChart = new Chart(ctx).Line(data, {animation: false, showTooltips: false, pointDot: false});

                setTimeout(doPoll, 30000);
            }
        });
    }
    doPoll();
});
