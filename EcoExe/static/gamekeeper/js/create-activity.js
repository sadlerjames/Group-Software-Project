function giveHidden(value) {
    document.querySelector("#hidden_"+value+"_activity_type").value = value;
};

$(document).ready(function(){
    $("#activity_selection").change(function(){
        $(this).find("option:selected").each(function(){
            var optionValue = $(this).attr("value");
            if(optionValue){
                $(".option").not("." + optionValue).hide();
                $("." + optionValue).show();
            } else{
                $(".option").hide();
            }
        });
    }).change();
});