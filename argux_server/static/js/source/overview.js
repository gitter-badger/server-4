$(function() {
    if (ARGUX_ACTION==='overview') {
        ctx = document.getElementById("overview").getContext("2d");
        overviewChart = new Chart(ctx, host_overview_chart_config);

        overviewChart.update();

        host.poll_overview();
    }
});
