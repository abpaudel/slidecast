var x = setInterval(updateslide, 2000)

function updateslide(){
  var request = new XMLHttpRequest();
  request.open('GET', 'http://'+ window.location.host + '/cast/getdata/');
  request.onload = function getdata(){
    var data = JSON.parse(request.responseText);
	PDFViewerApplication.pdfViewer.currentPageNumber = data.current_slide;
    };
  request.send();
  
}