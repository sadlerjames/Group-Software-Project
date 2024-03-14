$(document).ready(function() {
    
    let activity = 0; // Assuming the initial count is 0

    // executed when button is clicked by user
    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        activity++;

        // add a question input box to the DOM
        let option = $('<p>Activity ' + activity + ': <select name="extra_field_' + activity + '"></select></p>');
        $("[name=extra_field_count]").val(activity);
        $('#activities').append(option);
    });
});