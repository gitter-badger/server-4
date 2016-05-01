REST = {
    RESTCallType : {
        CREATE : "POST",
        READ : "GET",
        UPDATE : "POST",
        DELETE: "DELETE"
    },
    rest_call: function (url, type, success, error, complete) { 
        $.ajax({
            url: url,
            type: type,
            headers: { 'X-CSRF-Token': CSRF_TOKEN },
            dataType: "json",
            success: function(json) {
                success(json);
            },
            error: function(json) {
                error(json);
            },
            complete: function() {
                complete();
            }
        });
    }
};
