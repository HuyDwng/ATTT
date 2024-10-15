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