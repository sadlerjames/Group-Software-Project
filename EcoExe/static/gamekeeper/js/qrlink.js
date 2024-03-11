$(document).ready(function() {
    console.log("link");
    let qr_count = 0; // Assuming the initial count is 0
    // executed when button is clicked by user
    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        qr_count++;

        // add a question input box to the DOM
        let qr = $('<p>QR ' + qr_count + ': <input type="input" name="extra_field_' + qr_count + '" /></p>');
        $("[name=extra_field_count]").val(qr_count);
        $('#forms').append(qr);
    });
});