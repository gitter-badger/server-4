/* globals Chart: false */
/* globals ARGUX_BASE: false */

var config = {
    type: 'pie',
    data: {
        datasets: [
            {
                data: [
                    1,
                    0,
                    0,
                    0 ],
                backgroundColor: [
                    "#419641",
                    "#f0ad4e",
                    "#c12e2a",
                    "#e0e0e0"]
            }
        ],
        labels: [
            "Green",
            "Yellow",
            "Red",
            "Grey"
            ]
    },
    options: {
        responsive: true,
    }
};

// Get the context of the canvas element we want to select
var ctx = document.getElementById("overview").getContext("2d");
var myNewChart = new Chart(ctx, config);

$(function() {
    function doPoll() {
        $.ajax({
            url: ARGUX_BASE+"/rest/1.0/host",
            type: "GET",
            dataType: "json",
            success: function(json) {

                $('#hosts').empty();
                $.each(json.hosts, function(i, value) {
                    $('#hosts').append(
                        '<tr><td>' +
                        '<a href="'+ARGUX_BASE+'/host/' + value.name + '">' +
                        value.name +
                        '</a></td><td>' +
                        '<a href="'+ARGUX_BASE+'/host/' + value.name + '/alerts">' +
                        value.active_alerts+
                        '</a></td></tr>'
                    );
                });
                setTimeout(doPoll, 10000);
            }
        });
    }
    doPoll();
});
