document.getElementById('pay-button').addEventListener('click', function() {
    // Chuyển hướng sang trang thanh toán (thay 'payment.html' bằng URL của trang thanh toán)
    window.location.href = 'payment.html';
});

// Ẩn cảnh báo khi trang được tải
const seatWarning = document.getElementById('seat-warning');
seatWarning.style.display = 'none';
remainingSeats=20;

document.getElementById('guest-number').addEventListener('input', function() {
    const guestNumber = parseInt(this.value);
    const seatWarning = document.getElementById('seat-warning');
    
    // Kiểm tra giá trị nhập vào
    if (isNaN(guestNumber) || guestNumber === 0) {
        seatWarning.style.display = 'none'; // Ẩn thông báo nếu không có giá trị
    } else if (guestNumber > remainingSeats) {
        seatWarning.style.display = 'inline'; // Hiển thị thông báo nếu số lượng khách lớn hơn số ghế còn lại
    } else {
        seatWarning.style.display = 'none'; // Ẩn thông báo nếu số lượng khách hợp lệ
    }
});
