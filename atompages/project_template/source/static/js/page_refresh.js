$( document ).ready(function() {

  if ( window.location.href.indexOf('page_y') != -1 ) {
      var match = window.location.href.split('?')[1].split("&")[0].split("=");
      document.getElementsByTagName("body")[0].scrollTop = match[1];
  }

  window.refreshPage = function() {
    var page_y = document.getElementsByTagName("body")[0].scrollTop;
    window.location.href = window.location.href.split('?')[0] + '?page_y=' + page_y;
  }

  window.check_relaod = function(mtime){
      console.log(window.mtime, mtime);
      if(window.mtime == undefined) window.mtime = mtime;
      if(window.mtime && window.mtime < mtime){
        window.refreshPage();
      }
      setTimeout(window.get_mtime, 500);
  }

  window.get_mtime = function(){
    var requ = $.get("/mtime.html");
    requ.then(function(mtime){
      window.check_relaod(parseFloat(mtime))}
    );
    requ.error(function(){
      console.log("error checking mtime, retrying soon");
      setTimeout(window.get_mtime, 500);
    })
  }

  window.get_mtime();


});
