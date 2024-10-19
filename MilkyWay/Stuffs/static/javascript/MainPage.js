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

//run function
CountDownTimer()
