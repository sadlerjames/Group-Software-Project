$(document).ready(function() {
    let form_count = Number($("[name=extra_field_count]").val());
    let question_count = 0;

    //executed when button is clicked by user
    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        form_count ++;
        question_count ++;

        //add a question input box to the DOM
        let question = $('<p>Question ' + question_count + ': <input type ="text"/></p>');
        question.attr('name','extra_field_'+form_count);
        $("#forms").append(question);
        $("[name=extra_field_count]").val(form_count);
        
        //add 4 answer input box to the DOM
        for (let i=1; i <= 4; i++) {
            form_count ++;
            let element;
            if (i==1) {
                element = $('<p1>Correct Answer: <input type ="text"/></p1> ');
            } else {
                element = $('<p1>Answer: <input type ="text"/></p1> ');
            }
            element.attr('name','extra_field_'+form_count);
            $("#forms").append(element);
            $("[name=extra_field_count]").val(form_count);
        }
    });
});
