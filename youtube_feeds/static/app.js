$(function(){
  $("#btn-logout").on("click", function(e) {
    console.log("Logout");
    $.ajax({
      method: "POST",
      url: "logout",
      data: {"csrfmiddlewaretoken": crsf_token},
      success: function(data) {
        location.pathname = data.redirect_url;
      }
    });
  });
});
