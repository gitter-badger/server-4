function update_chart (obj, chart) {
    var hostname = 'localhost';
    var item = 'icmpping[env=local,addr=127.0.0.1,responsetime]';
    rest.call({
        url: ARGUX_BASE + 
             "/rest/1.0/host/" +
             hostname +
             "/item/" +
             item +
             "/details",
        });
    chart.update();
    setTimeout(
        update_chart,
        10000,
        obj,
        chart);
}

$(function() {
    $('.argux-chart').each(function (index) {
        var ctx = $(this)[0].getContext("2d");
        var chart = new Chart(ctx, history_chart_config);

        update_chart ($(this), chart);
    });
});
