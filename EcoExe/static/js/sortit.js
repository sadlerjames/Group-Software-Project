

// get a refrence to the canvas and its context
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

// newly spawned objects start at Y=25
var spawnLineY = 0;

// spawn a new object every 1500ms
var spawnRate = 1500;

// set how fast the objects will fall
var spawnRateOfDescent = 0.50;

// when was the last object spawned
var lastSpawn = -1;

// this array holds all spawned object
var objects = [];

// save the starting time (used to calc elapsed time)
var startTime = Date.now();

// start animating
animate();


function spawnRandomObject() {

  // select a random type for this new object
  var t;

  // About Math.random()
  // Math.random() generates a semi-random number
  // between 0-1. So to randomly decide if the next object
  // will be A or B, we say if the random# is 0-.49 we
  // create A and if the random# is .50-1.00 we create B

  if (Math.random() < 0.50) {
    t = "red";
  } else {
    t = "blue";
  }

  // create the new object
  var object = {
    // set this objects type
    type: t,
    // set x randomly but at least 15px off the canvas edges
    x: Math.random() * (canvas.width - 50),
    // set y to start on the line where objects are spawned
    y: spawnLineY,
  }

  // add the new object to the objects[] array
  objects.push(object);
}



function animate() {

  // get the elapsed time
  var time = Date.now();

  // see if its time to spawn a new object
  if (time > (lastSpawn + spawnRate)) {
    lastSpawn = time;
    spawnRandomObject();
  }

  // request another animation frame
  requestAnimationFrame(animate);

  // clear the canvas so all objects can be 
  // redrawn in new positions
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // draw the line where new objects are spawned
  ctx.beginPath();
  ctx.moveTo(0, spawnLineY);
  ctx.lineTo(canvas.width, spawnLineY);

  // move each object down the canvas
  for (var i = 0; i < objects.length; i++) {
    var object = objects[i];
    //if(!object.classList.contains("getting-sorted")){
        object.y += spawnRateOfDescent;
        ctx.beginPath();
        ctx.arc(object.x, object.y, 8, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fillStyle = object.type;
        ctx.fill();
    /*}
    else{
        //need to make it follow the mouse cursor
        console.log("being clicked");
    }*/
  }

}


/*rubbish = []

for(let i = 0; i < 10; i++){
    var trash = document.createElement("img");
    document.getElementById("fz2").appendChild(trash);

    trash.src = '../images/trash.png';
    trash.classList.add("trash");

    rubbish.add(trash);
}

function getOffset(el) {
    const rect = el.getBoundingClientRect();
    return {
      left: rect.left + window.scrollX,
      top: rect.top + window.scrollY
    };
  }

document.addEventListener('mousemove', function(e) {
    let body = document.querySelector('body');
    let circle = document.getElementById('circle');
    let left = e.offsetX;
    let top = e.offsetY;
    circle.style.left = left + 'px';
    circle.style.top = top + 'px';
  });
  */