$(function() {
    function doPoll() {
        $.ajax({
            url: "/argux/rest/1.0/host/"+argux_host,
            type: "GET",
            dataType: "json",
            success: function(json) {

                var categories = {'global':'', 'net':''};
                var alerts     = {'global':'', 'net':''};
                var collapsed  = {};


                // Build the panel contents.
                $.each(json.items, function(i, item) {

                    // Pick a category
                    if (item.category) {
                        category = item.category;
                    } else {
                        category = 'global';
                    }

                    // If name does not exist, show the key.
                    if (item.name != null) {
                        name = item.name
                    } else {
                        name = item.key
                    }

                    categories[category]+='<tr>'
                      + '<td>'
                      + '<a href="/host/'+argux_host+'/'+item.key+'/details">'
                      + name
                      + '</a>'
                      + '</td>'
                      + '<td></td>'
                      + '<td class="hidden-xs"></td>'
                      + '<td class="hidden-xs"></td>'
                      + '<td class="col-md-1 item-details">'
                      + '<a href="/host/'+argux_host+'/'+item.key+'/stats" aria-label="Stats">'
                      + '<span class="glyphicon glyphicon-stats" aria-hidden="true"></span>'
                      + '</a>&nbsp;'
                      + '<a href="/host/'+argux_host+'/'+item.key+'/details" aria-label="Details">'
                      + '<span class="glyphicon glyphicon-cog" aria-hidden="true"></span>'
                      + '</a>'
                      + '</td>'
                      + '</tr>';
                });

                // Determine if a panel was collapsed before the refresh.
                $('#items div.collapse').each(function(i, item) {
                    var id = item.id.substring(12);
                    collapsed[id] = $(this).hasClass('in');
                });

                // Remove all panels and build the page again.
                $('#items').empty();

                for (var key in categories) {
                    $('#items').append(
                        '<div class="panel panel-default">'
                        +'<div class="panel-heading">'
                        //+'<button class="btn btn-default btn-lr" '
                        +'<a '
                        +' data-toggle="collapse" data-target="#table-items-'+key+'">'
                        +key
                        +' <span class="badge">'+alerts[key]+'</span>'
                        +'</a>'
                        +'</div>'
                        +'<div class="collapse in" id="table-items-'+key+'">'
                        +'<table class="table table-striped">'
                        +'<thead>'
                        +'<tr>'
                        +'<th>Name</th>'
                        +'<th>Value</th>'
                        +'<th class="hidden-xs">Timestamp</th>'
                        +'<th class="hidden-xs">Last Checked</th>'
                        +'<th></th>'
                        +'</tr>'
                        +'</thead>'
                        +'<tbody>'
                        +'<tbody id="items-'+key+'">'
                        +'</tbody>'
                        +'</table>'
                        +'</div>'
                        +'</div>');

                    // Collapse panels that were collapsed before the refresh.
                    if (collapsed[key] == false) {
                        $('#table-items-'+key).removeClass('in');
                    }

                    // Add the panel-content.
                    $('#items-'+key).append(
                        categories[key]
                        );
                }
                /*
                $("#hosts tr").click(function() {
                    var href = $(this).find("a").attr("href");
                    if (href) {
                        window.location = href;
                    }
                });
                */
                setTimeout(doPoll, 5000);
            }
        });
    }
    doPoll();
});


