$(function(){function o(){setTimeout(monitors.get_monitors,6e4,{complete_callback:o,type:ARGUX_MONITOR_TYPE})}function t(o){$("#monitor-address").empty(),0==o.addresses.length?$("#monitor-address").append("<option disabled>No addresses</option>"):$.each(o.addresses,function(o,t){""!=t.description?$("#monitor-address").append('<option value="'+t.name+'">'+t.name+" ("+t.description+")</option>"):$("#monitor-address").append('<option value="'+t.name+'">'+t.name+"</option>")})}var e=$("#monitor-host").val();monitors.get_monitors({complete_callback:o,type:ARGUX_MONITOR_TYPE}),host.get_addresses({hostname:e,callback_success:t}),$("#monitor-form").submit(function(o){monitors.create({hostname:$("#monitor-host").val(),address:$("#monitor-address").val(),options:{interval:$("#monitor-interval").val()}}),monitors.get_monitors({type:ARGUX_MONITOR_TYPE})}),$("#monitor-delete-form").submit(function(o){monitors.remove({hostname:$("#dmcm-hostname").val(),address:$("#dmcm-address").val()}),$("#dmcm").modal("hide"),monitors.get_monitors({type:ARGUX_MONITOR_TYPE})}),$("#monitor-host").on("change",function(o){host.get_addresses({hostname:this.value,callback_success:t})})});
