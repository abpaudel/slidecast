
function updateslide(n){
  var csrftoken = $.cookie('csrftoken');
	var request = new XMLHttpRequest();
	request.open('POST', 'http://'+ window.location.host + '/cast/getdata/');
  request.setRequestHeader("Content-Type", "application/json");
  request.setRequestHeader("X-CSRFToken", csrftoken);
  var str = {"current_slide": n };
  request.send(JSON.stringify(str));
	
}

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function currentDiv(n) {
  showDivs(slideIndex = n);
}

function showDivs(n) {
  updateslide(n);
  var i;
  var x = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  if (n > x.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
     dots[i].className = dots[i].className.replace(" w3-red", "");
  }
  x[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " w3-red";
}


document.onkeydown = function(e) {
    e = e || window.event;
    switch(e.which || e.keyCode) {
        case 37: // left
          plusDivs(-1);
          break;

        case 38: // up
          
          break;
        case 39: // right
          plusDivs(1);
          break;

        case 40: // down
          break;

        default: return; // exit this handler for other keys
    }}