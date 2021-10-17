//slideshow js
var slideIndex = 1;
showSlides(slideIndex);

// change slide, -1 to go back a slide +1 to go forward
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// dot image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  } 
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  //changes classes on images and dots
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}
