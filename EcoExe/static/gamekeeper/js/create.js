$(document).ready(function() {
    let form_count = Number($("[name=extra_field_count]").val());
    console.log(form_count);

    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior
        form_count ++;
        let question = $('<br/><br/><p1>Question: </p1><input type ="text"/><br/>');
        question.attr('name','extra_field_'+form_count);
        $("#forms").append(question);
        $("[name=extra_field_count]").val(form_count);
        
        
        for (let i=1; i <= 4; i++) {
            form_count ++;
            let element = $('<p1>Answer: </p1><input type ="text"/> ');
            element.attr('name','extra_field_'+form_count);
            $("#forms").append(element);
            $("[name=extra_field_count]").val(form_count);
        }
        
    });
});
