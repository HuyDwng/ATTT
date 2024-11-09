// Chuyển hướng qua trang thanh toán
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('confirmation-popup').classList.add('disapear');
    document.getElementById('error-container').style.display = 'none';
});

// Xử lý khi kiểm tra thông tin có được điền đầy đủ hay chưa
document.getElementById('pay-button').addEventListener('click', function(event) {
    // Lấy tất cả các ô input bắt buộc
    const requiredInputs = document.querySelectorAll('.input-Name, .input-Email, .input-Number, .input-TourName, .input-GoDate, .input-BackDate');
    let allFilled = true;

    // Lấy khối thông báo lỗi
    const errorContainer = document.getElementById('error-container');

    // Kiểm tra xem các trường có rỗng hay không
    requiredInputs.forEach(input => {
        if (input.value.trim() === '') {
            input.classList.add('error'); // Thêm lớp 'error' nếu không có giá trị
            allFilled = false; // Đánh dấu là không đủ thông tin
            input.style.borderColor = "red"; // Đổi màu khung thành đỏ
        } else {
            input.classList.remove('error'); // Gỡ bỏ lớp 'error' nếu có giá trị
            input.style.borderColor = ""; // Khôi phục màu khung nếu đã nhập
        }
    });

    // Kiểm tra tính hợp lệ của các trường
    if (!allFilled) {
        // Hiện thông báo lỗi nếu không đủ thông tin
        errorContainer.style.display = 'block'; // Hiện khung thông báo
    } else {
        errorContainer.style.display = 'none'; // Ẩn khung thông báo nếu đủ thông tin
        // Hiển thị khối xác nhận
        document.getElementById('confirmation-popup').classList.remove('disapear');
    }
});

// Đóng thông báo lỗi
document.getElementById('close-error-btn').addEventListener('click', function() {
    document.getElementById('error-container').style.display = "none";
});

// Sự kiện khi nhấn nút "Kiểm tra lại"
document.getElementById('check-again-btn').addEventListener('click', function() {
    // Ẩn khối xác nhận và quay lại chỉnh sửa thông tin
    document.getElementById('confirmation-popup').classList.add('disapear');
});

// Sự kiện khi nhấn nút "Tiếp tục"
document.getElementById('proceed-btn').addEventListener('click', function() {
    // Chuyển sang trang thanh toán
    window.location.href = "payment.html"; // Trang bạn muốn chuyển tới
});
