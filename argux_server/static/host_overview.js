/* globals Chart: false */
/* globals ARGUX_BASE: false */
/* globals ARGUX_ACTION: false */

var config = {
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

// Get the context of the canvas element we want to select
var ctx;
var overviewChart;

function pollOverview() {
    $.ajax({
        url: ARGUX_BASE+"/rest/1.0/host",
        type: "GET",
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        success: function(json) {
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
                total_active_alerts+=value.active_alerts;
                if (value.severity === 'crit') {
                    graph_data[2] += 1;
                } else if (value.severity === 'warn') {
                    graph_data[1] += 1;
                } else if (value.severity === 'info') {
                    graph_data[3] += 1;
                } else {
                    graph_data[0] += 1;
                }
            });

            config.data.datasets[0].data = graph_data;

            if (total_active_alerts > 0) {
                $("#alert_count").text(total_active_alerts);
            } else {
                $("#alert_count").text('');
            }

            overviewChart.update();

            setTimeout(pollOverview, 10000);
        }
    });
}

$(function() {
    if (ARGUX_ACTION==='overview') {
        ctx = document.getElementById("overview").getContext("2d");
        overviewChart = new Chart(ctx, config);

        pollOverview();
    }
});
