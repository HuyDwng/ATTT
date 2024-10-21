let currentIndex = 0;
const slides = document.querySelectorAll('input[name="slider"]');
const numOfSlides = slides.length;

function autoSlide() {
    currentIndex = (currentIndex + 1) % numOfSlides;
    slides[currentIndex].checked = true;
}

// Chuyển slide mỗi 5 giây
setInterval(autoSlide, 3000);