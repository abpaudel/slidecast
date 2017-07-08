
var imagediv = document.getElementById('imagecontainer');
var buttondiv = document.getElementById('slide-button');
var nxtprevdiv = document.getElementById('nxtprev');


getslide();

function getslide(){
  var request = new XMLHttpRequest();
  request.open('GET', 'http://'+ window.location.host + '/present/getdata/');
  request.onload = function getdata(){
  var data = JSON.parse(request.responseText);
  renderHTML(data);
  showDivs(slideIndex = data.currentslide);
  };
  request.send();
  
}


function updateslide(isnew){
  var csrftoken = $.cookie('csrftoken');
	var request = new XMLHttpRequest();
	request.open('POST', 'http://'+ window.location.host + '/present/getdata/');
  request.setRequestHeader("Content-Type", "application/json");
  request.setRequestHeader("X-CSRFToken", csrftoken);
  var str = {"currentslide": isnew };
  request.send(JSON.stringify(str));
	
}



function renderHTML(data){
var htmlString1 = "";
var htmlString2 = "";
for (i = 1; i <= data.numberofslides; i++){
	htmlString1 += "<img class=\"mySlides\" src=\"../media/img/Slide" + i + ".JPG\"  style=\"width:100%\"/>";
	htmlString2 += "<button class=\"w3-button demo\" onclick=\"currentDiv(" + i + ")\">" + i + "</button>";
}

imagediv.insertAdjacentHTML('beforeend', htmlString1);
buttondiv.insertAdjacentHTML('beforeend', htmlString2);
nxtprevdiv.insertAdjacentHTML('beforeend', "<button class=\"w3-button w3-light-grey\" onclick=\"plusDivs(-1)\">❮ Prev</button><button class=\"w3-button w3-light-grey\" onclick=\"plusDivs(1)\">Next ❯</button>");

};


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

