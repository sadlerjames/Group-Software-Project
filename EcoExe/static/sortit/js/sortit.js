function getPositionAsNumVWH(str) {
  return Number(str.split("v")[0]);  //splits the attribute string if its stored in vh or vw
}

function getPositionAsNumPx(str) {
  return Number(str.split("p")[0]); //splits the attribute string if its stored in px
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

var btnStart = document.getElementById("btnStart");
var gameScreen = document.getElementById("game");
var btnExit = document.getElementById("btnExit");
var speedThreshold = 10;

var backgroundLoop = document.getElementById("background-loop");
var gameOver = document.getElementById("game-over");
var lifeLost = document.getElementById("life-lost");

// Add a click event listener to the button
btnStart.addEventListener("click", function() {
  gameScreen.style.display = "block";
  btnStart.style.display = "none";
  startGame();
});


var points = 0;
var lives = 3;
var intervalID;

var images = Array.from(document.querySelectorAll('.trash'));
const bin = document.getElementById('bin');
const bannerText = document.getElementById('banner-info');

document.addEventListener('mousemove', (e) => {
  // Calculate the offset of the mouse pointer relative to the container element
  const containerRect = document.getElementById('game').getBoundingClientRect();
  const mouseX = e.clientX - containerRect.left;

  // Set the position of the bin relative to the mouse pointer
  bin.style.left = mouseX + 'px';
});

document.addEventListener('touchstart', function(e) {
  initialX = e.touches[0].clientX - bin.offsetLeft;
});

document.addEventListener('touchmove', function(e) {
  e.preventDefault(); // Prevent default touch behavior (e.g., scrolling)
  
  currentX = e.touches[0].clientX - initialX;

  // Update the position of the DOM object
  if(currentX > 0 && currentX < screen.width - 40){
    bin.style.left = currentX + 'px'; //ensures the bin won't move offscreen - prevents scrolling so that the game is playable
  }


}, { passive: false });



// Define a function to update the positions of the objects
function moveObjects() {
  if(lives >= 1){
    images.forEach(function(image) {

      var pos;
      var opacity;
      var transition;

      if(image.style.top == ""){
        pos = 0;
      }
      else{
        pos = Number(getPositionAsNumVWH(image.style.top));
      }
  
      if(pos >= 90){
          //trash got to the sea, notify user 
          lifeLost.play();
          opacity = 0;
          lives -= 1;
          pos = 0; //reset image's position
          transition = 'top 0s'
          var newX = getRandomInt(20, 90); 
          image.style.left = newX + 'vw' //randomly set the x position
      }
      else{
          pos += (getRandomInt(1,speedThreshold)) / 2.5; // Adjust this value to control the speed of the movement
          opacity = 1;
          transition = 'top 0.2s'

          if(areElementsTouching(image, bin)){
              if(points == 0){
                points += 10;
              }
              else{
                points = Math.floor(points * 1.1);
              }
              opacity = 0;
              pos = 0; //reset image's position
              transition = 'top 0s'
              var newX = getRandomInt(20, 90); 
              image.style.left = newX + 'vw' //randomly set the x position
              if(points > 100){
                speedThreshold += 0.2;
              }
          }
      }
      bannerText.innerHTML = "Catch the rubbish before it falls in the quay!<br>Points: " + points + " Lives: " + lives;
      image.style.top = pos + 'vh';
      image.style.opacity = opacity;
      image.style.transition = transition;
    });
  }
  else{
    clearInterval(intervalID);
    backgroundLoop.pause();
    gameOver.play();
    gameScreen.style.display = "none";
    bannerText.textContent = "Game over! You scored " + points + " points - always remember to recycle properly.";
    btnExit.style.display = "block";

  }
}

function startGame(){
    points = 0;
    lives = 3;
    backgroundLoop.play();
    // Call the moveObjects function at regular intervals to update the positions
    intervalID = setInterval(moveObjects, 100); // Adjust the interval as needed (100 milliseconds)
}
