$(document).ready(function() {
    const reader = new Html5Qrcode('reader');
    var responseReceived = false;
    if(!responseReceived) {
        function qrCodeSuccessCallback(decodedText,decodedResult) {
            if(!responseReceived) {
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
                    // console.log(decodedText);
                    window.location.href = decodedText;
                    // getLocation({'getdata': JSON.stringify(decodedText)});
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
        fps:10,
        qrbox: qrboxFunction
    };

    reader.start({facingMode: "environment"},config,qrCodeSuccessCallback).catch(err => {alert(err);});


    reader.stop().catch(err => {
        alert('stop failed');
    });
});