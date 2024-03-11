console.log("Loaded 1");
// $(document).ready(function() {
//     let form_count = Number($("[name=extra_field_count]").val());

//     //event.preventDefault(); // Prevent default form submission behavior
//     form_count ++;
    
//     //add a dropdown for what activity for the qr to link to
//     let dropDown = $('<p1>Activity for the code to link to:  </p1><select form="create-qr" id="sel"><option value="quiz">Quiz</option></select>')
//     form_count ++;
//     dropDown.attr('name','extra_field_'+form_count);
//     $("#forms").append(dropDown);
//     $("[name=extra_field_count]").val(form_count);
//     //we then need to display more form elements depending on what option is selected

//     /*$("#sel").change(function(){
//         if(this.value=="quiz"){
//             console.log("Quiz selected");
//             let dropDown = $('<p1>Quiz for the code to link to:  </p1><select form="create-qr" id="quiz_sel"></select>')
//             form_count ++;
//             dropDown.attr('name','extra_field_'+form_count);
//             $("#forms").append(dropDown);
//             $("[name=extra_field_count]").val(form_count);
//             //we then need to display more form elements depending on what option is selected
            
//         }
//     });*/
// });
// $(document).ready(function(){
//     $("#activity_selection").change(function(){
//         $(this).find("option:selected").each(function(){
//             var optionValue = $(this).attr("value");
//             if(optionValue){
//                 $(".option").not("." + optionValue).hide();
//                 $("." + optionValue).show();
//             } else{
//                 $(".option").hide();
//             }
//         });
//     }).change();
// });
$(document).ready(function() {
    console.log("Loaded");
    function giveHidden(value) {
        console.log("WORKS");
        document.querySelector("#hidden_activity_type input").value = value;
    };
});