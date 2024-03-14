const x = document.getElementById("demo");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);

  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  var long  = position.coords.latitude;
  var lat = position.coords.longitude;
  console.log(long);
  fetch("/treasurehunt/validate", {
    method: "POST",
    headers: {},
    body: JSON.stringify({ longitude:long, latitude:lat})
  });
}