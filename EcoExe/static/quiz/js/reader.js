const reader = new Html5Qrcode('reader');
function qrCodeSuccessCallback(decodedText,decodedResult) {
	var csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
	function csrfSafeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	
	$.ajaxSetup({
		beforeSend: function(xhr,settings) {
			if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader('X-CSRFToken',csrftoken);
			}
		}
	});
	
	$.ajax({
		url: "{% url 'get_quiz' %}",
		data: {
			'getdata': JSON.stringify(decodedText),
		},
		dataType: 'json',
		success: function(res,status) {
			alert(res);
			alert('success');
			alert(status);
		},
		error: function(err) {
			alert('error');
			alert(err.status);
		}
	});
	/*
	console.log(decodedResult);
	alert(decodedText);*/
}
const config = {
	fps:10,
	qrbox: {
		width:250,
		height:250
	}
};

reader.start({facingMode:'user'},config,qrCodeSuccessCallback).catch(err => {alert(err);});


reader.stop().catch(err => {
	alert('stop failed');
});