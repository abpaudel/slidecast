var imagediv = document.getElementById('imagecontainer');
var request = new XMLHttpRequest();
request.open('GET', 'http://'+ window.location.host + '/present/getdata');
request.onload = function(){
	var data = JSON.parse(request.responseText);
	renderHTML(data);
};
request.send();

function renderHTML(data){
var htmlString = "";
for (i = 1; i <= data.numberofslides; i++){

	//htmlString += "<div><img src=\"../media/img/Slide" + i + ".JPG\"/></div>";
}

//imagediv.insertAdjacentHTML('beforeend', htmlString);

};

