// Đếm
let count = 0;

        function increase() {
            count++;
            document.getElementById('counter').innerText = count;
        }

        function decrease() {
            if (count > 0) {
                count--;
                document.getElementById('counter').innerText = count;
            }
        }
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

function decrease() {
    var qty = document.getElementById('quantity');
    if (parseInt(qty.value) > 1) {
        qty.value = parseInt(qty.value) - 1;
    }
}

function increase() {
    var qty = document.getElementById('quantity');
    var max = parseInt(qty.getAttribute('max'));
    if (parseInt(qty.value) < max) {
        qty.value = parseInt(qty.value) + 1;
    }
}

