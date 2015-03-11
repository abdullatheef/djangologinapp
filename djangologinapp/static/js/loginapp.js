
function gSignIN(appDomainUrl){
  $('#g_button').hide();
  $('#g_button_area').html("<h3>Please wait ...</h3>")
    $.get(appDomainUrl + "getGData", function(data, status){
        if (status=="success" && JSON.parse(data).result==200){
        	gUrl = JSON.parse(data).url;
        	window.location.href = gUrl;
        }
		else{
      $('#g_button').show();
      $('#g_button_area').hide()
			$("#err_msg").html("<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>"
  				+"<span class='sr-only'>Error:</span>"
  				+"Something went wrong in server</div>");
		}
    });
	}