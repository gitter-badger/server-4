$(function(){"overview"===ARGUX_ACTION&&(ctx=document.getElementById("overview").getContext("2d"),overviewChart=new Chart(ctx,host_overview_chart_config),overviewChart.update(),host.poll_overview())});