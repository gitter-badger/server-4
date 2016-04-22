/* globals ARGUX_BASE: false */
/* globals CSRF_TOKEN: false */


$(function() {
    $('a.dns-remove').click(function() {
        var domain = $(this).attr('data-domain');
        $.ajax({
            url: ARGUX_BASE+
                 "/rest/1.0/monitor/"+
                 ARGUX_MONITOR_TYPE+
                 "/"+
                 ARGUX_MONITOR_HOST+
                 "/"+
                 ARGUX_MONITOR_ADDR+
                 "/domain/"+
                 domain
                 ,
            type: "DELETE",
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            success: function() {
            },
            error: function() {
            }
        });
    });
    $('a.dns-edit').click(function() {
        $('#monitor-domain').val($(this).attr('data-domain'));
        $('#monitor-domain').attr('readonly', true);
        $('#dns-domain-modal').modal('show');
        $('#monitor-domain-A').prop('checked', $(this).attr('data-domain-a'));
        $('#monitor-domain-AAAA').prop('checked', $(this).attr('data-domain-aaaa'));
        $('#monitor-domain-MX').prop('checked', $(this).attr('data-domain-mx'));
    });
    $('#dns-domain-modal').on('hidden.bs.modal', function () {
        $('#monitor-domain').val('');
        $('#monitor-domain').attr('readonly', false);
        $('#monitor-domain-A').prop('checked', false);
        $('#monitor-domain-AAAA').prop('checked', false);
        $('#monitor-domain-MX').prop('checked', false);
    });

    $('#dns-domain-form').submit(function(event) {
        var domain = $('#monitor-domain').val();
        var check_a = $('#monitor-domain-A').is(':checked');
        var check_aaaa = $('#monitor-domain-AAAA').is(':checked');
        var check_mx = $('#monitor-domain-MX').is(':checked');
        $.ajax({
            url: ARGUX_BASE+
                 "/rest/1.0/monitor/"+
                 ARGUX_MONITOR_TYPE+
                 "/"+
                 ARGUX_MONITOR_HOST+
                 "/"+
                 ARGUX_MONITOR_ADDR+
                 "/domain/"+
                 domain
                 ,
            type: "POST",
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            data: '{'+
                    '"types":{'+
                      '"A":'+JSON.stringify(check_a)+','+
                      '"AAAA":'+JSON.stringify(check_aaaa)+','+
                      '"MX":'+JSON.stringify(check_mx)+
                    '}'+
                  '}',
            success: function() {
                $('#dns-domain-modal').modal('hide');
                return true;
            },
            error: function() {
                $('#trigger-form-alerts').append(
                    '<div class="alert alert-danger alert-dismissible">'+
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                    '<strong>Problem:</strong> Domain could not be created.'+
                    '</div>'
                );
            }
            
        });
    });
});
