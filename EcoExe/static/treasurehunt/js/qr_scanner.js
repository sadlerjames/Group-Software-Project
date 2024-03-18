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
                        getLocation({'getdata': JSON.stringify(decodedText)});
                        // const readerdiv = document.getElementById('reader');
                        // const questiondiv = document.getElementById('questiondiv');
                        // let score = 0;
                        // readerdiv.hidden = true;
                        // questiondiv.hidden = false;
                        
                        // const question = document.createElement('h2');
                        // const answerlist = document.createElement('ul');
                        
                        // function* getQuestion(quiz, question_index) { // generator 
                        // 	while(question_index < quiz['questions'].length) {
                        // 		question.appendChild(document.createTextNode(quiz['questions'][question_index]));
                        // 		questiondiv.appendChild(question);
                        // 		//console.log(question_index);
                                
                        // 		for(var i in quiz['answers'][question_index]) {
                        // 			let answernode = document.createElement('li');
                        // 			let answerbutton = document.createElement('input');
                        // 			answerlist.appendChild(answernode);
                        // 			answerbutton.type='button';
                        // 			answerbutton.value=quiz['answers'][question_index][i]; // adds choice to button
                                    
                        // 			if(i == quiz['correct'][question_index]) { // checks if index of correct answer is the same as the correct choice
                        // 				answerbutton.onclick = function() {
                        // 					alert('correct');
                        // 					answerlist.innerHTML = ''; // clears list
                        // 					question.innerHTML = ''; // clears question
                        // 					answered = true;
                        // 					question_iterator.next();
                        // 					//console.log(question_iterator.next().value); // goes to next question
                        // 				}
                        // 			} else {
                        // 				answerbutton.onclick = function() {
                        // 					alert('faillllll');
                        // 					answerlist.innerHTML = ''; // clears list
                        // 					question.innerHTML = ''; // clears question
                        // 					answered = true;
                        // 					question_iterator.next();
                        // 					//console.log(question_iterator.next().value); // goes to next question
                        // 				}
                        // 			}
                        // 			answernode.appendChild(answerbutton);
                        // 		}

                        // 		questiondiv.appendChild(answerlist);
                        // 		yield question_index;
                        // 		question_index++;
                        // 	}
                        // }
                        
                        //var question_iterator = getQuestion(res, 0);
                        
                        //question_iterator.next();
                        //console.log(question_iterator.next().value);
                        //console.log(question_iterator.next().value);
                
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