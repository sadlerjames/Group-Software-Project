$(document).ready(function() {
    const reader = new Html5Qrcode('reader');
    var responseReceived = false;
    if(!responseReceived) {
        function qrCodeSuccessCallback(decodedText,decodedResult) {
            if(!responseReceived) {
                var domain = window.location.protocol + '//' + window.location.host;
                var fullUrl = domain + decodedText;
                
                responseReceived = true;
                    var csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
            
                function getResponseReceived() {
                    return responseReceived;
                }
                
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
                    console.log("errored after");
                    // console.log(fullUrl);
                    window.location.href = fullUrl;
                    // getLocation({'getdata': JSON.stringify(fullUrl)});
            }
        }
    }

    let qrboxFunction = function(viewfinderWidth, viewfinderHeight) {
        let minEdgePercentage = 0.7; // 70%
        let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
        let qrboxSize = Math.floor(minEdgeSize * minEdgePercentage);
        return {
            width: qrboxSize,
            height: qrboxSize
        };
    }

    const config = {
        fps: 10,
        qrbox: qrboxFunction,
        aspectRatio: 1
    };

    reader.start({facingMode: "environment"},config,qrCodeSuccessCallback).catch(err => {alert(err);});

    /*reader.stop().catch(err => {
        alert('stop failed');
    });*/
});