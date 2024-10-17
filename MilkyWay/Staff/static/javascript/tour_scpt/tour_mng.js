// Biến để lưu trữ hàng sẽ bị xóa
let rowToDelete = null;

// Hàm gắn sự kiện xóa cho tất cả các nút "Xóa"
function attachDeleteListeners() {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach((button) => {
        button.addEventListener('click', function () {
            rowToDelete = this.closest('tr'); // Lưu hàng chứa nút "Xóa" này
            document.getElementById('confirmModal').style.display = 'block'; // Hiển thị modal
        });
    });
}

// Sự kiện đóng modal
document.querySelector('.close-button').addEventListener('click', function () {
    document.getElementById('confirmModal').style.display = 'none'; // Ẩn modal
});


// Xử lý nút "Xóa" trong modal
document.getElementById('confirmDelete').addEventListener('click', function () {
    if (rowToDelete) {
        rowToDelete.remove(); // Xóa hàng khỏi bảng
        rowToDelete = null; // Reset biến
    }
    document.getElementById('confirmModal').style.display = 'none'; // Ẩn modal
});
//Xử lý nút hủy
document.getElementById('cancelDelete').addEventListener('click', function () {

    document.getElementById('confirmModal').style.display = 'none'; // Ẩn modal
});
// Sự kiện khi người dùng nhấn ngoài modal
window.addEventListener('click', function (event) {
    const modal = document.getElementById('confirmModal');
    if (event.target === modal) {
        modal.style.display = 'none'; // Ẩn modal nếu nhấn bên ngoài
    }
});


// Gọi hàm để gắn sự kiện khi tải trang
document.addEventListener('DOMContentLoaded', function () {
    attachDeleteListeners();
});
