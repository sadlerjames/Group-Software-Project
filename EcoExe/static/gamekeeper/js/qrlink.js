$(document).ready(function() {
    let qr_count = Number($("[name=extra_field_count]").val());

    //executed when button is clicked by user
    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        qr_count ++;
        console.log("incrementing");

        //add a question input box to the DOM
        let qr = $('<p>QR ' + qr_count + ': <input type ="input"/></p>');
        qr.attr('name','extra_field_'+qr_count);
        $("[name=extra_field_count]").val(qr_count);
        console.log($("[name=extra_field_count]"));
        $('#forms').append(qr);
    });
});
