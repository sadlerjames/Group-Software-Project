$(document).ready(function() {
    let form_count = Number($("[name=extra_field_count]").val());

    //event.preventDefault(); // Prevent default form submission behavior
    form_count ++;
    
    //add a dropdown for what activity for the qr to link to
    let dropDown = $('<p1>Activity for the code to link to:  </p1><select form="create-qr" id="sel"><option value="quiz">Quiz</option></select>')
    form_count ++;
    dropDown.attr('name','extra_field_'+form_count);
    $("#forms").append(dropDown);
    $("[name=extra_field_count]").val(form_count);
    //we then need to display more form elements depending on what option is selected

    $("#sel").change(function(){
        if(this.value=="quiz"){
            /*
            let dropDown = $('<p1>Quiz for the code to link to:  </p1><select form="create-qr" id="quiz_sel"></select>')
            form_count ++;
            dropDown.attr('name','extra_field_'+form_count);
            $("#forms").append(dropDown);
            $("[name=extra_field_count]").val(form_count);
            //we then need to display more form elements depending on what option is selected
            */
        }
    });
    


});
