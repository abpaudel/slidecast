var x = setInterval(updateslide, 2000)

function updateslide(){
  var request = new XMLHttpRequest();
  request.open('GET', 'http://'+ window.location.host + '/cast/getdata/');
  request.onload = function getdata(){
    var data = JSON.parse(request.responseText);
    currentDiv(data.current_slide);
    //console.log(data.current_slide);
    };
  request.send();
  
}

// function uncheck(){
//   var chkbox= document.getElementById('chkbox');
//   chkbox.checked = false;
//   clearInterval(x);

// }

// function autosync(element){
// 	if (element.checked) {x = setInterval(updateslide, 5000); element.checked = false;}
// 	else { clearInterval(x); element.checked = false;}

// }


function plusDivs(n) {
  showDivs(slideIndex += n);
}

function currentDiv(n) {
  showDivs(slideIndex = n);
}

function showDivs(n) {
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