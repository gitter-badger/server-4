/* globals ARGUX_BASE: false */
/* globals CSRF_TOKEN: false */


$(function() {
    $('a.dns-edit').click(function() {
        switch ($(this).attr('data-domaintype')) {
            case 'A':
            case 'AAAA':
            case 'MX':
                var span = $(this).children('span');
                span.toggleClass('glyphicon-unchecked');
                span.toggleClass('glyphicon-check');
                break;
            default:
                $('#monitor-domain').val($(this).attr('data-domain'));
                $('#monitor-domain').attr('readonly', true);
                $('#dns-domain-modal').modal('show');
        }
    });
    $('#dns-domain-form').submit(function(event) {
        alert($('#monitor-domain').val());
    });
    $('#dns-domain-modal').on('hidden.bs.modal', function () {
        $('#monitor-domain').val('');
        $('#monitor-domain').attr('readonly', false);
    });
});
