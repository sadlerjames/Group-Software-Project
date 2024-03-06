function getPosAsNum(str) {
  return(str.split("v")[0]);
}

var images = Array.from(document.querySelectorAll('.trash'));

images.forEach(
  (image) => 
  {
      image.addEventListener('click', function() {
          if(image.classList.contains("being-held")){
              image.classList.remove("being-held");
          }
          else{
              image.classList.add("being-held");
          }
  })
}
);


document.addEventListener('mousemove', function(event) {
  images.forEach(function(image) {
    if (image.classList.contains("being-held")) {
      image.style.left = event.clientX + 'px';
      image.style.top = event.clientY + 'px';
    }
    else{
      
    }
  });
});


// Iterate over each image and move them down
for (var i = 0; i < images.length; i++) {
  
  console.log("hello");
  var image = images[i];
  
  var position = 0;
  // Set interval to move the image down every 100 milliseconds
  setInterval(function() {
      var pos = getPosAsNum(image.style.top);
      if(image.classList.contains("being-held")){
          //need to make the image follow the mouse pointer
      }
      else{
          if(pos >= 90){
              //image.classList.add("hidden");
              position = 0;
              image.style.top = 0 + 'vh'; //reset image's position
              //image.classList.remove("hidden");
          }
          else{
              position += 0.5; // Adjust this value to control the speed of the movement
              image.style.top = position + 'vh';
          }
          
      }

      
      //console.log(position);
}, 100);

}