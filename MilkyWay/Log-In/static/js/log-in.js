$(document).ready(function(){
    $('#eye').click(function(){
        $(this).toggleClass('open')
        $(this).children('i').toggleClass('fa-eye-slash fa-eye');
        if($(this).hasClass('open')){
            $(this).prev().attr('type','text');
        }
        else  $(this).prev().attr('type','password');
    });
});

// validation form login
const inputUsername = document.querySelector("#username");
const inputPassword = document.querySelector("#password");
const btnLogin = document.querySelector(".submit");
// validation form login

btnLogin.addEventListener("click", (e) => {
  e.preventDefault();
  if (inputUsername.value === "" || inputPassword.value === "") {
    alert("Vui lòng không được để trống!");
  } else {
    const user = JSON.parse(localStorage.getItem(inputUsername.value));
    if (
      user.username === inputUsername.value &&
      user.password === inputPassword.value
    ) {    
        alert("Đăng nhập thành công");
        window.location.href = "../BTLlater.html"
    } else {
        alert("Đăng nhập thất bại");
        window.location.href = "./log-in.html"
  }
}});

$(document).ready(function () {
  // Chức năng gọi khi người dùng đăng nhập bằng Google
  window.onload = function () {
      gapi.load('auth2', function () {
          gapi.auth2.init({
              client_id: 'YOUR_CLIENT_ID.apps.googleusercontent.com',
              scope: 'email'
          });
      });
  };

  // Chức năng đăng nhập
  $('.g_id_signin').on('click', function () {
      const auth2 = gapi.auth2.getAuthInstance();
      auth2.signIn().then(function (user) {
          const id_token = user.getAuthResponse().id_token;
          $.ajax({
              type: 'POST',
              url: '/auth-receiver/',
              data: {
                  'credential': id_token,
                  'csrfmiddlewaretoken': '{{ csrf_token }}'  // Gửi token CSRF
              },
              success: function (response) {
                  // Xử lý thành công
                  window.location.href = '/';  // Redirect đến trang chính hoặc trang mong muốn
              },
              error: function (error) {
                  // Xử lý lỗi
                  console.error('Error:', error);
              }
          });
      });
  });
});
