/* globals Chart: false */
/* globals moment: false */
/* globals ARGUX_BASE: false */
/* globals ARGUX_HOST: false */
/* globals ARGUX_ITEM: false */
/* globals ARGUX_ITEM_ACTION: false */
/* globals TIMESPAN: false */
/* globals CSRF_TOKEN: false */

var chart_start_time = null;
var chart_end_time = 'now';

var dataset_avg = {
    label: 'Average',
    borderWidth: 1,
    borderColor: "rgba(10,145,115,1)",
    backgroundColor: "rgba(10,200,160,0.2)",
    pointHoverRadius: 4,
    data: [{'x': '0', 'y': '1'}]
};
var dataset_min = {
    label: 'Min',
    borderWidth: 1,
    borderColor: "rgba(145,115,10,1)",
    backgroundColor: "rgba(200,200,10,0.2)",
    pointHoverRadius: 4,
};
var dataset_max = {
    label: 'Max',
    borderWidth: 1,
    borderColor: "rgba(145,10,115,1)",
    backgroundColor: "rgba(200,10,200,0.2)",
    pointHoverRadius: 4,
};

var unit = {};
var item_unit_prefix='';

var config = {
    type: 'line',
    data: {
        datasets: [
            dataset_avg,
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
                    displayFormats: {
                        'millisecond': 'SSS [ms]',
                        'second': 'HH:mm:ss', // 23:20:01
                        'minute': 'MM/DD HH:mm', // 23:20:01
                        'hour': 'YY/MM/DD HH:00', // 2015/12/22 23:00
                        'day': 'YY/MM/DD', // 2015/12/22
                        'month': 'MMM YYYY', // Sept 2015
                        'quarter': '[Q]Q - YYYY', // Q3 - 2015
                        'year': 'YYYY', // 2015
                    },
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
                    callback: function(value) {
                        if(unit.symbol){
                            return ''+Math.round(value*10)/10+' '+item_unit_prefix+unit.symbol;
                        } else {
                            return ''+Math.round(value*10)/10;
                        }
                    }
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
            },
            point: {
                radius: 1
            }
        },
    }
};

var ctx;
var chart;

function pollItemValues(showValues, showAlerts, callback) {

    var start_time = moment().subtract(30, 'minutes');

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
        if(TIMESPAN==='1M') {
            start_time = now.subtract(1, 'months');
        }

        chart_start_time = start_time.format('YYYY-MM-DDTHH:mm:ss');
    } else {
    }


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
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        success: function(json) {
            callback(json);
            if(json.active_alerts > 0) {
                $("#alert_count").text(json.active_alerts);
            } else {
                $("#alert_count").text('');
            }
        },
        complete: function() {
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
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        success: function(json) {
            $('#triggers').empty();
            $.each(json.triggers, function(i, trigger) {
                var last_alert = '-'
                if (trigger.last_alert === 'now') {
                    last_alert = '<span data-toggle="tooltip" data-placement="bottom" ' +
                    'title="Still active">Now</span>';
                } else if (trigger.last_alert !== null) {
                    last_alert = '<span data-toggle="tooltip" data-placement="bottom" ' +
                    'title="'+trigger.last_alert+'">' +
                    moment(trigger.last_alert).fromNow() +
                    '</span>';
                }
                $('#triggers').append(
                    '<tr class=""><td>' +
                    '<span class="glyphicon glyphicon-none"></span> ' +
                    '<a href="#">' +
                    trigger.name +
                    '</a>' +
                    '</td><td>' +
                    trigger.rule +
                    '</td><td>' +
                    last_alert +
                    '<button ' +
                    ' class="pull-right trigger-del btn btn-xs borderless"' +
                    ' data-toggle="tooltip"' +
                    ' data-trigger-id="' + trigger.id + '"' +
                    ' title="Remove Trigger">' +
                    '<span class="glyphicon glyphicon-remove"></span>' +
                    '</button>' +
                    '</td></tr>'
                );
            });
            $(".trigger-del").on('click', function(evt) {
                $.ajax({
                    timeout: 5000,
                    url: ARGUX_BASE+
                         "/rest/1.0/host/"+
                         ARGUX_HOST+
                         "/item/"+
                         ARGUX_ITEM+
                         "/trigger/"+
                         evt.target.getAttribute("data-trigger-id"),
                    type: "DELETE",
                    headers: { 'X-CSRF-Token': CSRF_TOKEN },
                    success: function() {
                        return true;
                    },
                    error: function() {
                        $('#trigger-form-alerts').append(
                            '<div class="alert alert-danger alert-dismissible">'+
                            '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                            '<strong>Problem:</strong> Trigger rule could not be deleted.'+
                            '</div>'
                        );
                    }
                });
            });
            if(json.active_alerts > 0) {
                $("#alert_count").text(json.active_alerts);
            } else {
                $("#alert_count").text('');
            }
        },
        complete: function() {
            setTimeout(pollTriggers, 3000);
        }
    });

}

function validateTrigger(trigger) {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/host/"+
             ARGUX_HOST+
             "/item/"+
             ARGUX_ITEM+
             "/trigger/validate",
        type: "POST",
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        data: '{'+
              '"name": '+JSON.stringify(trigger.name)+',' +
              '"rule": '+JSON.stringify(trigger.rule)+
              '}',
        success: function(json) {
            if (json.valid === true) {
                createTrigger(trigger);
            } else {
                $('#trigger-form-alerts').empty();
                $('#trigger-form-alerts').append(
                    '<div class="alert alert-danger alert-dismissible">'+
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                    '<strong>Problem:</strong> Trigger rule could not be validated:<br>'+
                    json.error+
                    '</div>'
                );
            }
        },
        error: function(json) {
            $('#trigger-form-alerts').empty();
            $('#trigger-form-alerts').append(
                '<div class="alert alert-danger alert-dismissible">'+
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                '<strong>Problem:</strong> Trigger rule could not be validated:<br>'+
                json.error+
                '</div>'
            );
        }
    });
}

function createTrigger(trigger) {
    $.ajax({
        url: ARGUX_BASE+
             "/rest/1.0/host/"+
             ARGUX_HOST+
             "/item/"+
             ARGUX_ITEM+
             "/trigger",
        type: "POST",
        headers: { 'X-CSRF-Token': CSRF_TOKEN },
        dataType: "json",
        data: '{'+
              '"name": '+JSON.stringify(trigger.name)+',' +
              '"rule": '+JSON.stringify(trigger.rule)+',' +
              '"description": '+JSON.stringify(trigger.description)+',' +
              '"severity": '+JSON.stringify(trigger.severity) +
              '}',
        success: function() {
            $('#create-monitor-modal').modal('hide');
            return true;
        },
        error: function() {
            $('#monitor-form-alerts').append(
                '<div class="alert alert-danger alert-dismissible">'+
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                '<strong>Problem:</strong> Monitor could not be created.'+
                '</div>'
            );
        }
    });
}

function details_cb(json) {
    var datapoints = [];

    datapoints.push({
            x: json.start_time,
            });

    chart_start_time = json.start_time;

    $('#datetimepicker1').data('DateTimePicker').date(chart_start_time);
    $('#datetimepicker2').data('DateTimePicker').date(chart_end_time);

    if (json.unit) {
        unit = json.unit;
        //config.options.scales.yAxes[0].ticks.suggestedMax = 100;
        if (json.max_value < 0.1 && json.min_value > -0.1) {
            item_unit_prefix = 'm';
        }
        if (json.max_value < 0.0001 && json.min_value > -0.0001) {
            item_unit_prefix = '\u{00B5}';
        }
        if (json.max_value > 100 && json.min_value < -100) {
            item_unit_prefix = 'k';
        }
        if (json.max_value > 1000000 && json.min_value < -100000) {
            item_unit_prefix = 'M';
        }
        if (json.max_value > 1000000000 && json.min_value < -100000000) {
            item_unit_prefix = 'G';
        }
    }
    if (json.values) {
        $.each(json.values.avg, function(i, value) {
            switch (item_unit_prefix) {
                case '\u{00B5}':
                    item_value = (value.value*1000000);
                    break;
                case 'm':
                    item_value = (value.value*1000);
                    break;
                default:
                    item_value = value.value
            }
            item_value = Math.round(item_value*100)/100;

            datapoints.push({
                x: value.ts,
                y: item_value});
        });
        datapoints.push({
                x: json.end_time,
                });

        dataset_avg.data = datapoints;
    }


    chart.update();
}

function alerts_cb(json) {

    $('#alerts').empty();

    if (json.alerts) {
        $.each(json.alerts, function(i, al) {
            var icon = 'glyphicon-none';
            var severity = 'info';
            var ack;

            if (al.severity === "crit") {
                severity = "danger";
                icon = 'glyphicon-exclamation-sign';
            }
            if (al.severity === "warn") {
                severity = "warning";
                icon = 'glyphicon-exclamation-sign';
            }

            if(al.acknowledgement === null) {
                ack = 'No (<a href="#">Acknowledge</a>)';
            } else {
                ack = 'Yes (<a href="#">Show Ack</a>)';
            }

            $('#alerts').append(
                '<tr class="'+severity+'"><td>' +
                '<span class="glyphicon '+icon+'"></span> ' +
                '<a href="#">' +
                al.name +
                '</a>' +
                '</td><td>' +
                moment(al.start_time).fromNow(true) +
                '</td><td>' +
                ack +
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
        $('#datetimepicker1').datetimepicker({
            date: moment().subtract(30, 'minutes'),
            useCurrent: false //Important! See issue #1075
        });
        $('#datetimepicker2').datetimepicker({
            date: moment(),
            useCurrent: false //Important! See issue #1075
        });
        $("#datetimepicker1").on("dp.change", function (e) {
            $('#datetimepicker2').data("DateTimePicker").minDate(e.date);
            chart_start_time = e.date.format('YYYY-MM-DDTHH:mm:ss');
            TIMESPAN='';
        });
        $("#datetimepicker2").on("dp.change", function (e) {
            $('#datetimepicker1').data("DateTimePicker").maxDate(e.date);
            chart_end_time = e.date.format('YYYY-MM-DDTHH:mm:ss');
            TIMESPAN='';
        });
        pollItemValues(true, false, details_cb);
    }
    if (ARGUX_ITEM_ACTION==="alerts") {
        pollItemValues(false, true, alerts_cb);
    }
    if (ARGUX_ITEM_ACTION==="triggers") {

        $('#trigger-form').submit(function(event) {
            event.preventDefault();
            trigger = {
                'name': $('#trigger-name').val(),
                'rule': $('#trigger-rule').val(),
                'description': $('#trigger-desc').val(),
                'severity': $('#trigger-severity').val()
            };
            validateTrigger(trigger);
        });
        pollTriggers();
    }
});
