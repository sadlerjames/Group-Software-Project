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

async function getLocations(csrfToken) {
    var allCoordinates = [];

    // First HTTP request
    fetch("/treasurehunt/next_locations/", {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Process the data from the first request
        processData(data, "first");
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

    // Second HTTP request
    fetch("/treasurehunt/new_locations/", {
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Process the data from the second request
        processData(data, "second");
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

    // Get data needed for each pinpoint
    function processData(data, source) {
        for (var key in data) {
            var name = data[key][0];
            var coordinates = data[key][1];
            var parts = coordinates.split(',');
            var latitude = parts[0];
            var longitude = parts[1];

            allCoordinates.push({
                name: name,
                latitude: latitude,
                longitude: longitude,
                source: source,
                info: data[key][2],
                image: data[key][3]
            });
        }

        // Populate map with pinpoints
        initMap(allCoordinates);
    }
}

// Load map with pinpoints
async function initMap(coordinates) {
    const { Map, InfoWindow } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

    // Map config
    const map = new Map(document.getElementById("google-maps-display"), {
        center: {lat: 50.737273546349144, lng: -3.5351586176728236},
        zoom: 14,
        mapId: "5d7ba1c59311dfdd",
        streetViewControl: false,
        fullscreenControl: false,
    });

    const infoWindow = new InfoWindow();

    // Create a separate scope for each iteration of the loop
    for (let i = 0; i < coordinates.length; i++) {
        (function() {
            let point = coordinates[i];

            // Setn background colour depending on whether it is a new or in progress hunt
            let pinBackground;
            if (point.source === "first") {
                pinBackground = new PinElement({
                    background: "#003c3c",
                    borderColor: "#ffffff",
                    glyphColor: "#00dca5",
                });
            } else if (point.source === "second") {
                pinBackground = new PinElement({
                    background: "#00dca5",
                    borderColor: "#ffffff",
                    glyphColor: "#003c3c",
                });
            }

            var marker = new AdvancedMarkerElement({
                map,
                position: { lat: parseFloat(point.latitude), lng: parseFloat(point.longitude) },
                title: point.name,
                content: pinBackground.element,
            });

            // Popup when clicking a pinpoint
            marker.addListener("click", ({ domEvent, latLng }) => {
                const { target } = domEvent;

                infoWindow.close();
                infoWindow.setContent('<h3>' + marker.title + '</h3><br><p style="color: black;">Location: ' + point.info + '</p><br><img src="/media/' + point.image + '">');
                infoWindow.open(marker.map, marker);
            });
        })();
    }

    // Close info window when clicking on the map
    map.addListener("click", () => {
        infoWindow.close();
    });
}



