function update_chart (obj, chart, config) {
    var chart_id = obj.data('graphid');

    rest.call({
        url: ARGUX_BASE + 
             "/rest/1.0/graph/" +
             chart_id +
             "?get_values=true",
        dataType: "json",
        success: function(json) {
            obj.children(".heading").children(".title").text(json.name);
            config.data.datasets = [];

            counter = 0;
            // Set data for each item separately.
            $.each(json.items, function(i, item) {
                var dataset = {
                    label: item.name,
                    borderWidth: 1,
                    pointHoverRadius: 4,
                    data: [{'x': '0', 'y': '1'}]
                };
                var datapoints = [];
                if(item.color !== undefined){
                    color = item.color;
                } else {
                    pc = get_palette_color(counter);
                    color = pc[0];
                    counter = pc[1];
                }

                dataset['borderColor'] = color;
                dataset['backgroundColor'] = hex2rgba(color, 0.1);

                $.each(item.values.avg, function(i, value) {
                    datapoints.push({
                        x: value.ts,
                        y: value.value});
                });

                dataset.data = datapoints;

                config.data.datasets.push(dataset)
            });
            chart.update();
        },
        complete: function() {
            setTimeout(
                update_chart,
                10000,
                obj,
                chart,
                config);
        }
    });
}

$(function() {
    $('.argux-chart').each(function (index) {
        var obj = $(this);

        var chart_obj  = obj.children('.chart-body');
        var canvas = $('<canvas/>');
        chart_obj.append(canvas);
        var ctx = canvas[0].getContext("2d");

        // Create a copy of the history_chart_config so we can use
        // a different configuration for each chart.
        var config = $.extend(true, {}, history_chart_config);
        var chart = new Chart(ctx, config);

        update_chart (obj, chart, config);
    });
});
