$(document).ready(function() {
    let form_count = Number($("[name=extra_field_count]").val());

    //executed when button is clicked by user
    $("#add-another-qr").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        form_count ++;

        //add a qr code name input box to the DOM
        let qrCodeName = $('<br/><br/><p1>QR Code Name: </p1><input type ="text"/><br/>');
        qrCodeName.attr('name','extra_field_'+form_count);
        $("#forms").append(qrCodeName);
        $("[name=extra_field_count]").val(form_count);
        
        //add a dropdown for what activity for the qr to link to
        let dropDown = $('<p1>Activity for the code to link to:  </p1><select form="create-qr"><option value="quiz">Quiz</option></select>')
        form_count ++;
        dropDown.attr('name','extra_field_'+form_count);
        $("#forms").append(dropDown);
        $("[name=extra_field_count]").val(form_count);
    });
});
