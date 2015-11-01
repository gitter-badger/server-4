/* globals Chart: false */
/* globals ARGUX_HOST: false */

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
            url: "/argux/rest/1.0/host",
            type: "GET",
            dataType: "json",
            success: function(json) {

                $('#hosts').empty();
                $.each(json.hosts, function(i, value) {
                    $('#hosts').append(
                        '<tr><td>' +
                        '<a href="/host/' + value.name + '">' +
                        value.name +
                        '</a></td><td>' +
                        '0' +
                        '</td></tr>'
                    );
                });
                setTimeout(doPoll, 10000);
            }
        });
    }
    doPoll();
});
