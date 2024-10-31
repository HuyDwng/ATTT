function showTab(evt, tabName) {
    // Hide all tab contents
    var tabContent = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }

    // Remove active class from all tabs
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }

    // Show current tab and add active class
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


// Lấy các phần tử HTML theo ID
var hoursEl = document.getElementById('hours');
var minutesEl = document.getElementById('minutes');
var secondsEl = document.getElementById('seconds');

function Clock() {
    const now = new Date();

    // Gán các giá trị thời gian hiện tại vào các phần tử HTML
    hoursEl.innerText = String(now.getHours()).padStart(2, '0');
    minutesEl.innerText = String(now.getMinutes()).padStart(2, '0');
    secondsEl.innerText = String(now.getSeconds()).padStart(2, '0');
}

// Cập nhật đồng hồ mỗi giây
setInterval(Clock, 1000);

// scroll navbar
var menu = document.getElementById("Menu");

//scroll top
var gototop = document.getElementById("Gototop");
//change title menu
let sections = document.querySelectorAll('body > section');
let navLinks = document.querySelectorAll('header ul a');
window.onscroll = () =>{
    //change title menu
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop -150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if(top >= offset && top < offset + height){
            navLinks.forEach(links => {
                links.classList.remove('active-menu');
                document.querySelector('header ul a[href*=' + id + ']').classList.add('active-menu');
            })
        }
    });
    // scroll navbar
    console.info(document.documentElement.scrollTop);
    if (document.documentElement.scrollTop > 100) {
        menu.style.background = "rgba(38, 38, 38, 0.9)"; // Đặt nền đen khi cuộn trang
    } else {
        menu.style.background = "transparent"; // Làm nền trong suốt khi quay về đầu trang
    }


//scroll top
    console.info(document.documentElement.scrollTop);
    if(document.documentElement.scrollTop > 100){
        gototop.style.display = "block";
    }
    else{
       gototop.style.display = "none";
    }
}
function goToTop(){
   var x= setInterval(function(){
       document.documentElement.scrollTop-=40;
       if(document.documentElement.scrollTop<=0)
       clearInterval(x);
   },1)
}

//run function
CountDownTimer()
goToTop()

let currentIndex = 0;
const slides = document.querySelectorAll('input[name="slider"]');
const numOfSlides = slides.length;

function autoSlide() {
    currentIndex = (currentIndex + 1) % numOfSlides;
    slides[currentIndex].checked = true;
}

// Chuyển slide mỗi 5 giây
setInterval(autoSlide, 3000);
