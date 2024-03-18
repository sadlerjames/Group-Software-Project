function getPosAsNum(str) {
  return(str.split("v")[0]);
}

function getRandomInt(min, max) { 
  min = Math.ceil(min); 
  max = Math.floor(max); 
  return Math.floor(Math.random() * (max - min + 1)) + min; 
} 

var images = Array.from(document.querySelectorAll('.trash'));

document.addEventListener('mousemove', (e) => {
  const object = document.getElementById('bin');
  object.style.left = e.offsetX + 'px';
});

document.addEventListener('touchstart', function(e) {
  const object = document.getElementById('bin');
  initialX = e.touches[0].clientX - object.offsetLeft;
});

document.addEventListener('touchmove', function(e) {
  e.preventDefault(); // Prevent default touch behavior (e.g., scrolling)
  
  currentX = e.touches[0].clientX - initialX;

  // Update the position of the DOM object
  const object = document.getElementById('bin');
  object.style.left = currentX + 'px';
  
}, { passive: false });



// Define a function to update the positions of the objects
function moveObjects() {
  images.forEach(function(image) {

    var pos;
    if(image.style.top == ""){
      pos = 0;
    }
    else{
      var pos = Number(getPosAsNum(image.style.top));
    }
    

    if(pos >= 90){
        pos = 0; //reset image's position
        var newX = getRandomInt(20, 90); 
        image.style.left = newX + 'vw' //randomly set the x position
    }
    else{
        pos += (getRandomInt(1,10)) / 2.5; // Adjust this value to control the speed of the movement
    }
    image.style.top = pos + 'vh';
  });
}

// Call the moveObjects function at regular intervals to update the positions
setInterval(moveObjects, 100); // Adjust the interval as needed (100 milliseconds)


