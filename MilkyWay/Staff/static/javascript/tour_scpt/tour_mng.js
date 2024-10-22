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


/*===========================================Lấy dữ liệu==================================== */



// Sử dụng path.join để tạo đường dẫn tương đối
const filePath = '../../static/data/tour_data/tour_data.json'

fetch(filePath)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(tours => {
        const htmlContent = generateHTMLTable(tours);
        document.querySelector('tbody').innerHTML = htmlContent; // Thêm HTML vào tbody
    })
    .catch(error => console.error('There has been a problem with your fetch operation:', error));

// Hàm tạo HTML
function generateHTMLTable(tours) {
    let html = '';

    tours.forEach(tour => {
        html += `
        <tr>
            <td>${tour.tour_name}</td>
            <td>${tour.departure_date}</td>
            <td>${tour.return_date}</td>
            <td>${tour.total_tickets}</td>
            <td>${tour.remaining_tickets}</td>
            <td>${tour.price} VND</td>
            <td>
                <a class="edit-btn" href="../../templates/tour_management/tour_edit.html" target="_blank">Sửa</a>
                <button class="delete-btn">Xóa</button>
                <a class="more-info-btn" href="#">Xem chi tiết</a>
            </td>
        </tr>`;
    });

    return html;
}
