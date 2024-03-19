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

fetch("/treasurehunt/next_locations/", {
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
    var allCoordinates = [];

    for (var key in data) {

                
        var coordinates = data[key];
        var parts = coordinates.split(',');

        // Extract the values into separate variables
        var longitude = parts[1];
        var latitude = parts[0];
        allCoordinates.push([longitude, latitude]);
    }

    initMap(allCoordinates);

})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});


function initMap(coordinates) {
    const myLatLng = { lat: parseInt(coordinates[0][0]), lng: parseInt(coordinates[0][1]) };
    const map = new google.maps.Map(document.getElementById("google-maps-display"), {
      zoom: 12,
      center: myLatLng,
    });
  
    new google.maps.Marker({
      position: myLatLng,
      map,
      title: "Hello World!",
    });
  }
  
//   window.initMap = initMap;