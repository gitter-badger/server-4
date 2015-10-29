/* globals Chart: false */
/* globals ARGUX_HOST: false */

var config = {
    type: 'pie',
    data: {
        datasets: [
            {
                data: [
                    12,
                    1,
                    1,
                    4 ],
                backgroundColor: [
                    "#0f0",
                    "#ff0",
                    "#f00",
                    "#ddd"]
            }
        ],
        labels: [
            "Red",
            "Green",
            "Yellow",
            "Grey",
            "Dark Grey"
            ]
    },
    options: {
        responsive: true,
        elements: {
            line: {
                tension: 0.3
            }
        },
    }
};

// Get the context of the canvas element we want to select
var ctx = document.getElementById("overview").getContext("2d");
var myNewChart = new Chart(ctx, config);
