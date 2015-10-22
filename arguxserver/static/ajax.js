$(function() {
    function doPoll() {
        $.ajax({
            url: "/argux/rest/1.0/host",
            type: "GET",
            dataType: "json",
            success: function(json) {
                $('#hosts').empty();
                $.each(json['hosts'], function(i, item) {
                    $('#hosts').append("<tr><td><a href='/host/"+item+"'>"+item+"</a></td><td></td></tr>");
                });
                /*
                $("#hosts tr").click(function() {
                    var href = $(this).find("a").attr("href");
                    if (href) {
                        window.location = href;
                    }
                });
                */
                setTimeout(doPoll, 15000);
            }
        });
    }
    doPoll();
});

