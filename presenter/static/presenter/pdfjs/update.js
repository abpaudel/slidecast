
document.addEventListener('pagechange', function(e) {
  if (e.pageNumber !== e.previousPageNumber) {
    var csrftoken = $.cookie('csrftoken');
    var request = new XMLHttpRequest();
    request.open('POST', 'http://'+ window.location.host + '/cast/getdata/');
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("X-CSRFToken", csrftoken);
    var str = {"current_slide": e.pageNumber };
    request.send(JSON.stringify(str));
  }
});