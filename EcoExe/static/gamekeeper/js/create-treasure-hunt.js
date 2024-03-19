$(document).ready(function() {
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie starts with the name we're looking for
            if (cookie.startsWith(name + '=')) {
                // Return the cookie value
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        // Return null if the cookie with the specified name is not found
        return null;
        
    }
      
    const csrfToken = getCookie('csrftoken');

    let activity = 0; // Assuming the initial count is 0

    // executed when button is clicked by user
    $("#add-another").click(function(event){
        event.preventDefault(); // Prevent default form submission behavior

        fetch("/gamekeeper/treasurehunt/get_activities", {
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json" 
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let storedActivities = data;

            activity++;

            var activityOptions = "";

            for (var key in storedActivities) {
                
                // Access the object inside the current key
                var innerObject = storedActivities[key];

                var id = innerObject['act_id'];
                var name = innerObject['name'];

                var html = '<option value="' + id + '">' + name + '</option>'; 
                activityOptions += html;     
            }

            // add a question input box to the DOM
            let option = $('<p>Activity ' + activity + ': <select name="extra_field_' + activity + '">' + activityOptions  + '</select></p>');
            $("[name=extra_field_count]").val(activity);
            $('#activities').append(option);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
}); 