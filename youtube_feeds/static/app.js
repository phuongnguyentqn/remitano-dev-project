$(function(){
  const $btnLogout = $("#btn-logout");
  const $btnLogin = $("#btn-login");
  const $formLogin = $("#form-login");

  // Handle click login
  $btnLogin.on("click", function(e) {
    e.preventDefault();
    console.log("Click Login");
    var data = {};
    $formLogin.serializeArray().forEach(function(v) {
      data[v.name] = v.value;
    })
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
});
