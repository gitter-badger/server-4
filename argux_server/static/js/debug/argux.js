var argux = {
    VERSION: "0.0.1"
};

REST={RESTCallType:{CREATE:"POST",READ:"GET",UPDATE:"POST",DELETE:"DELETE"},rest_call:function(E,T,e,n,c){$.ajax({url:E,type:T,headers:{"X-CSRF-Token":CSRF_TOKEN},dataType:"json",success:function(E){e(E)},error:function(E){n(E)},complete:function(){c()}})}};