$(document).ready(function() {
    let form_count = Number($("[name=extra_field_count]").val());
    let question_count = 0;

    // use event delegation for toggle button clicks
    $("#forms").on("click", ".toggle-button", function() {
        $(this).closest('p').next('.question-container').toggle();
    });

    //executed when button is clicked by user
    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        form_count ++;
        question_count ++;

        // button to collapse a question for ease of use
        let button = $('<p><button type="button" class="toggle-button">Collapse/Expand Question ' + question_count + '</button></p>');
        $("#forms").append(button);

        // create a div to contain the question and answer inputs
        let questionContainer = $('<div>');
        questionContainer.addClass('question-container');

        //add a question input box to the DOM
        let question = $('<p>Question ' + question_count + ': <input type ="text" name="extra_field_' + form_count + '" /></p>');
        //question.attr('name','extra_field_'+form_count);
        $("[name=extra_field_count]").val(form_count);
        questionContainer.append(question);
        
        //add 4 answer input box to the DOM
        for (let i=1; i <= 4; i++) {
            form_count ++;
            let element;
            if (i==1) {
                element = $('<p1>Correct Answer: <input type ="text" name="extra_field_' + form_count + '"/></p1> ');
            } else {
                element = $('<p1>Answer: <input type ="text" name="extra_field_' + form_count + '"/></p1> ');
            }
            //let qr = $('<p>QR ' + qr_count + ': <input type="input" name="extra_field_' + qr_count + '" value="Hello"/></p>');
            $("[name=extra_field_count]").val(form_count);
            questionContainer.append(element);
        }

        $("#forms").append(questionContainer);
    });
});
