var ctx = null;
var overviewChart = null;

function update_complete_callback() {
    overviewChart.update();

    setTimeout(host.get_host_overview, 10000, {'complete_callback' : update_complete_callback});
}

$(function() {
    if (ARGUX_ACTION==='overview') {
        ctx = document.getElementById("overview").getContext("2d");
        overviewChart = new Chart(ctx, host_overview_chart_config);

        host.get_host_overview({'complete_callback': update_complete_callback});
    }
});
