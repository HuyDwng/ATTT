/* Thanh toán */
// Giả lập dữ liệu từ database (có thể thay thế bằng dữ liệu từ API)
const paymentData = {
    id: 1,
    booking_id: 12345,
    amount: 500000, // 500.000 VND
    payment_date: "2024-10-20",
    payment_status: "pending", // Trạng thái ban đầu là 'pending'
    payment_method: null,
};

// Hiển thị thông tin thanh toán
document.getElementById("bookingId").textContent = paymentData.booking_id;
document.getElementById("amount").textContent = paymentData.amount;
document.getElementById("paymentDate").textContent = paymentData.payment_date;
document.getElementById("paymentStatus").textContent = paymentData.payment_status;

// Xử lý sự kiện submit form thanh toán
document.getElementById("paymentForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Lấy phương thức thanh toán từ form
    const selectedMethod = document.querySelector('input[name="paymentMethod"]:checked').value;

    // Cập nhật phương thức thanh toán vào dữ liệu
    paymentData.payment_method = selectedMethod;

    // Cập nhật trạng thái thanh toán (ở đây giả lập là successful)
    paymentData.payment_status = "successful";

    // Cập nhật thông tin trạng thái trên giao diện
    document.getElementById("paymentStatus").textContent = paymentData.payment_status;

    // Thông báo cho người dùng
    alert("Thanh toán thành công bằng phương thức: " + selectedMethod + "\nSố tiền: " + paymentData.amount + " VND");

    // Sau đó có thể thực hiện các hành động tiếp theo, ví dụ: gửi thông tin lên server
});

/* Xử lý sự kiện đếm ngược thời gian */
// Thiết lập thời gian đếm ngược (ví dụ 10 phút)
let countdownTime = 900; // Thời gian đếm ngược tính bằng giây
let countdownInterval;

// Hàm hiển thị thời gian đếm ngược
function updateCountdown() {
    let minutes = Math.floor(countdownTime / 60);
    let seconds = countdownTime % 60;
    document.getElementById("countdown").textContent = 
        (minutes < 10 ? "0" : "") + minutes + ":" + 
        (seconds < 10 ? "0" : "") + seconds;
    
    if (countdownTime <= 0) {
        clearInterval(countdownInterval); // Dừng đếm ngược
        document.getElementById("timeout-modal").style.display = 'block'; // Hiển thị popup
    }
    countdownTime--; // Giảm thời gian đếm ngược
}

// Bắt đầu đếm ngược
countdownInterval = setInterval(updateCountdown, 1000);

// Xử lý khi người dùng nhấn "Quay lại trang chủ"
document.getElementById('return-home').onclick = function() {
    window.location.href = '../templates/index.html'; // Thay đổi đường dẫn trang chủ
};

// Đóng popup khi nhấn ngoài nội dung (nếu cần)
window.onclick = function(event) {
    const modal = document.getElementById('timeout-modal');
    if (event.target == modal) {
        modal.style.display = 'none'; // Đóng popup
    }
};


