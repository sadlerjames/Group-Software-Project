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

function getLocations(csrfToken) {
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
        console.log(data);
    
        for (var key in data) {
    
            var name = data[key][0];
            var coordinates = data[key][1];
            var parts = coordinates.split(',');
    
            // Extract the values into separate variables
            var latitude = parts[0];
            var longitude = parts[1];
            
            allCoordinates.push([name, latitude, longitude, data[key][2], data[key][3]]);
        }
    
        initMap(allCoordinates);
    
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}



async function initMap(coordinates) {
    const { Map, InfoWindow } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
        "marker",
    );

    const map = new Map(document.getElementById("google-maps-display"), {
        center: {lat: 50.737273546349144, lng: -3.5351586176728236},
        zoom: 14,
        mapId: "5d7ba1c59311dfdd",
        streetViewControl: false,
        fullscreenControl: false,
      });

    // Create an info window to share between markers.
    const infoWindow = new InfoWindow();

    for (let i = 0; i < coordinates.length; i++) {
        let point = coordinates[i];

        console.log(point);


        const pinBackground = new PinElement({
            background: "#003c3c",
            borderColor: "#ffffff",
            glyphColor: "#00dca5",
        });

        var marker = new AdvancedMarkerElement({
            map,
            position: { lat: parseFloat(point[1]), lng: parseFloat(point[2]) },
            title: point[0],
            content: pinBackground.element,
        });

        // Add a click listener for each marker, and set up the info window.
        marker.addListener("click", ({ domEvent, latLng }) => {
            const { target } = domEvent;

            infoWindow.close();
            infoWindow.setContent('<h3>' + marker.title + '</h3><br><p style="color: black;">Location: ' + point[3] + '</p><br><img src="/media/' + point[4] + '">');
            infoWindow.open(marker.map, marker);
        });
    }
  }
//   window.initMap = initMap;

  window.addEventListener('load', function() {
    getLocations(csrfToken);
})

