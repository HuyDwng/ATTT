function increase(type) {
    var element = document.getElementById(type);
    var currentValue = parseInt(element.textContent);
    if (currentValue < 15) {
      element.textContent = currentValue + 1;
    }
  }
  
  function decrease(type) {
    var element = document.getElementById(type);
    var currentValue = parseInt(element.textContent);
    if (currentValue > 0) {
      element.textContent = currentValue - 1;
    }
  }
// Lấy tất cả các phần tử img-item
const imgItems = document.querySelectorAll('.img-item img');

// Lấy phần tử ảnh lớn
const mainImage = document.querySelector('.image img');

// Lặp qua tất cả các ảnh nhỏ và thêm sự kiện click
imgItems.forEach(item => {
    item.addEventListener('click', function() {
        // Khi click vào ảnh nhỏ, thay đổi src của ảnh lớn
        mainImage.src = this.src;
    });
});
