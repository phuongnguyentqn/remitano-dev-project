$(function(){
  const $btnLogout = $("#btn-logout");
  const $btnLogin = $("#btn-login");
  const $formLogin = $("#form-login");
  const $btnShare = $("#btn-share");
  const $formShare = $("#form-share-video");

  // Handle click login
  $btnLogin.on("click", function(e) {
    e.preventDefault();
    console.log("Click Login");
    // TODO: Check required input
    var data = {};
    $formLogin.serializeArray().forEach(function(v) {
      data[v.name] = v.value;
    });
    $.ajax({
      method: "POST",
      url: "login-register",
      data: data,
      success: function(data) {
        location.pathname = data.redirect_url;
      },
      error: function(err) {
        alert(err.responseJSON.message);
      }
    });
  });
  // Handle click logout
  $btnLogout.on("click", function(e) {
    console.log("Click Logout");
    $.ajax({
      method: "POST",
      url: "logout",
      data: {"csrfmiddlewaretoken": crsf_token},
      success: function(data) {
        location.pathname = data.redirect_url;
      }
    });
  });
  // Handle click share
  $btnShare.on("click", function(e) {
    e.preventDefault();
    console.log("Click Share");
    // TODO: Check required input
    var data = {};
    $formShare.serializeArray().forEach(function(v) {
      data[v.name] = v.value;
    });
    console.log(data);
    $.ajax({
      method: "POST",
      url: "do-share",
      data: data,
      success: function(data) {
        location.pathname = data.redirect_url;
      },
      error: function(err) {
        alert(err.responseJSON.message);
        $formShare.find('input[name=url]').val("");
      }
    });
  });
});
