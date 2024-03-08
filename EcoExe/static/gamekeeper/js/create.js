$(document).ready(function() {
    let form_count = Number($("[name=extra_field_count]").val());

    //executed when button is clicked by user
    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        form_count ++;

        //add a question input box to the DOM
        let question = $('<br/><br/><p>Question: </p><input type ="text"/><br/>');
        question.attr('name','extra_field_'+form_count);
        $("#forms").append(question);
        $("[name=extra_field_count]").val(form_count);
        
        //add 4 answer input box to the DOM
        for (let i=1; i <= 4; i++) {
            form_count ++;
            let element = $('<p>Answer: </p><input type ="text"/> ');
            element.attr('name','extra_field_'+form_count);
            $("#forms").append(element);
            $("[name=extra_field_count]").val(form_count);
        }
    });
});
