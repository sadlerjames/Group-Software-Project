function getPosAsNum(str) {
  return(str.split("v")[0]);
}

function getRandomInt(min, max) { 
  min = Math.ceil(min); 
  max = Math.floor(max); 
  return Math.floor(Math.random() * (max - min + 1)) + min; 
} 

function areElementsTouching(element1, element2) {
  let rect1 = element1.getBoundingClientRect();
  let rect2 = element2.getBoundingClientRect();

  return !(
    rect1.bottom < rect2.top ||
    rect1.top > rect2.bottom ||
    rect1.right < rect2.left ||
    rect1.left > rect2.right
  );
}

var points = 0;
var images = Array.from(document.querySelectorAll('.trash'));
const bin = document.getElementById('bin');
const bannerText = document.getElementById('banner-info');

document.addEventListener('mousemove', (e) => {
  bin.style.left = e.offsetX + 'px';
});

document.addEventListener('touchstart', function(e) {
  initialX = e.touches[0].clientX - bin.offsetLeft;
});

document.addEventListener('touchmove', function(e) {
  e.preventDefault(); // Prevent default touch behavior (e.g., scrolling)
  
  currentX = e.touches[0].clientX - initialX;

  // Update the position of the DOM object
  bin.style.left = currentX + 'px';
  
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
        if(areElementsTouching(image, bin)){
            console.log("CAUGHT!");
            if(points == 0){
              points += 10;
            }
            else{
              points = Math.floor(points * 1.1);
            }
            
            bannerText.textContent = "Catch the rubbish before it falls in the sea! Points: " + points;
            pos = 0; //reset image's position
            var newX = getRandomInt(20, 90); 
            image.style.left = newX + 'vw' //randomly set the x position
        }
    }
    image.style.top = pos + 'vh';
  });
}

// Call the moveObjects function at regular intervals to update the positions
setInterval(moveObjects, 100); // Adjust the interval as needed (100 milliseconds)


