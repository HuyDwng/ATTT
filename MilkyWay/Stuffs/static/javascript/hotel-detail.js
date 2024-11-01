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

// TOGGLE ACCORDITION

function toggleAccordion(element) {
  const item = element.parentElement;
  const content = item.querySelector('.accordion-content');
  const isOpen = item.classList.contains('open');

  // Đóng tất cả các accordion khác nếu cần
  document.querySelectorAll('.accordion-item').forEach(el => {
      if (el !== item) {
          el.classList.remove('open');
          el.querySelector('.accordion-content').style.maxHeight = '0';
          el.querySelector('.accordion-content').style.padding = '0 15px';
      }
  });

  // Toggle trạng thái open của item hiện tại
  item.classList.toggle('open');

  if (!isOpen) {
      content.style.maxHeight = content.scrollHeight + 'px';
      content.style.padding = '15px';
      
      // Thêm preventDefault để ngăn nhảy lên đầu nếu sự kiện click gây ra
      if (event && event.preventDefault) {
          event.preventDefault();
      }
  } else {
      content.style.maxHeight = '0';
      content.style.padding = '0 15px';
  }
}