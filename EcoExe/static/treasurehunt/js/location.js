const x = document.getElementById("demo");


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
console.log(csrfToken);


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

  fetch("/treasurehunt/validate/", {
    method: "POST", 
    headers: {
      "X-CSRFToken": csrfToken,
      "Content-Type": "application/json" 
    },
    body: JSON.stringify({ 
      longitude:long, 
      latitude:lat})
  }).catch(error => {
      console.error('Error:', error);
  });
}