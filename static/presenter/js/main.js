var imagediv = document.getElementbyId("imagecontainer")
var request = new XMLHttpRequest()
request.open('GET', 'http://'+ window.location.hostname + 'present/getdata')
request.onload = function(){
	data = JSON.parse(request.responseText);
	console.log(data)
}
request.send()

var htmlString = ""
for (i = 0; i < data.numberofslides; i++){
	htmlString += '<div><img src="../media/img/Slide" + i+1 + ".JPG"/></div>'

}

imagediv.insertAdjacentHTML(htmlString)

