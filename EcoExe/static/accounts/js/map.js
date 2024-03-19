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

        var name = data[key][0];
        var coordinates = data[key][1];
        var parts = coordinates.split(',');

        // Extract the values into separate variables
        var latitude = parts[0];
        var longitude = parts[1];
        
        allCoordinates.push([name, latitude, longitude]);
    }

    initMap(allCoordinates);

})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});


function initMap(coordinates) {
    const map = new google.maps.Map(document.getElementById("google-maps-display"), {
      zoom: 14.5,
      center: {lat: 50.737273546349144, lng: -3.5351586176728236},
    });

    setMarkers(map, coordinates);
  }

  function setMarkers(map, coordinates) {
    for (let i = 0; i < coordinates.length; i++) {
        let point = coordinates[i];
    
        new google.maps.Marker({
          position: { lat: parseFloat(point[1]), lng: parseFloat(point[2]) },
          map,
        //   icon: image,
        //   shape: shape,
          title: point[0],
        //   zIndex: beach[3],
        });
    }

  }
  
//   window.initMap = initMap;