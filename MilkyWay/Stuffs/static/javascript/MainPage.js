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


// CountDown Timer
var daysEl = document.getElementById('days')
var hoursEl = document.getElementById('hours')
var minutesEl = document.getElementById('minutes')
var secondsEl = document.getElementById('seconds')

function CountDownTimer(){
    const countdownDate = new Date("Nov 30, 2024 23:59:59").getTime();

    //convert to milliseconds
    const second = 1000
    const minute = second * 60
    const hour = minute * 60
    const day = hour * 24
    
    //Calculate every second
    const interval = setInterval(() =>{
        // Get Current Date
        const now = new Date(). getTime()
        const distance = countdownDate - now

        daysEl.innerText = formatNumber(Math.floor(distance / day))
        hoursEl.innerText = formatNumber(Math.floor((distance % day) / hour))
        minutesEl.innerText = formatNumber(Math.floor((distance % hour) / minute))
        secondsEl.innerText = formatNumber(Math.floor((distance % minute) / second))

        //when data is reached
        if(distance < 0){
            document.getElementById('countdown').style.display = 'none'

            //stop interval
            clearInterval(interval)
        }
    },1000)

}

function formatNumber(number){
    if(number < 10){
        return '0' + number
    }

    return number
}

// scroll navbar
var menu = document.getElementById("Menu");

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
        menu.style.background = "black"; // Đặt nền đen khi cuộn trang
    } else {
        menu.style.background = "transparent"; // Làm nền trong suốt khi quay về đầu trang
    }
}







//run function
CountDownTimer()
