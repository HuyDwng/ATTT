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
$(document).ready(function(){
    $('#eye-again').click(function(){
        $(this).toggleClass('open')
        $(this).children('i').toggleClass('fa-eye-slash fa-eye');
        if($(this).hasClass('open')){
            $(this).prev().attr('type','text');
        }
        else  $(this).prev().attr('type','password');
    });
});

//hàm signup
const inputUsernameRegister = document.querySelector("#username");
const inputPasswordRegister = document.querySelector("#password");
const inputPasswordRegister_1 = document.querySelector("#password-1");
const btnRegister = document.querySelector(".submit");
const btn_close = document.querySelector('#btn-close');

btnRegister.addEventListener("click", (e) => {
  e.preventDefault();
  if (
    inputUsernameRegister.value === "" ||
    inputPasswordRegister.value === ""
  ) {
    alert("Vui lòng không để trống");
  } else {
    if (inputPasswordRegister.value === inputPasswordRegister_1.value){
    // array user
    const user = {
      username: inputUsernameRegister.value,
      password: inputPasswordRegister.value,
    };
    let json = JSON.stringify(user);
    localStorage.setItem(inputUsernameRegister.value, json);
    alert("Đăng kí thành công");
    window.location.href="./log-in.html"
  }
  else{
    alert("Mật khẩu nhập lại không trùng khớp!")
  }
}});

