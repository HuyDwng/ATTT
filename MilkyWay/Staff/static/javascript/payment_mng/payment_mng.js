// Lấy dữ liệu===================================================================================

const filePath = 'payment_data.json';

let transactions = [];

// Fetch the data from the JSON file
fetch(filePath)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        transactions = data; // Lưu trữ dữ liệu giao dịch
        displayTransactions(transactions); // Hiển thị tất cả giao dịch ban đầu
    })
    .catch(error => console.error('There has been a problem with your fetch operation:', error));

// Hàm hiển thị giao dịch
// function displayTransactions(transactions) {
//     const htmlContent = generateHTMLTable(transactions);
//     document.querySelector('tbody').innerHTML = htmlContent; // Thêm HTML vào tbody
// }

// Hàm tạo HTML
// function generateHTMLTable(transactions) {
//     let html = '';

//     transactions.forEach(transaction => {
//         html += `
//        <tr>
//             <td>${transaction.transaction_id}</td>
//             <td>${transaction.customer_name}</td>
//             <td>${transaction.tour_name}</td>
//             <td>${transaction.transaction_date}</td>
//             <td>${transaction.total_payment}</td>
//             <td>${transaction.transaction_status}</td>
//             <td>${transaction.payment_method}</td>
//             <td>
//                 <details>
//                     <summary class="btn btn-link p-0">Xem chi tiết</summary>
//                     <div class="details-content">
//                         <span class="close-btn" onclick="this.closest('details').removeAttribute('open')">&times;</span>
//                         <p>Chi tiết giao dịch ${transaction.transaction_id}:</p>
//                         <ul>
//                             <li>Mã giao dịch: ${transaction.transaction_id}</li>
//                             <li>Tên khách hàng: ${transaction.customer_name}</li>
//                             <li>Tên tour: ${transaction.tour_name}</li>
//                             <li>Ngày giao dịch: ${transaction.transaction_date}</li>
//                             <li>Tổng số tiền: ${transaction.total_payment}</li>
//                             <li>Trạng thái: ${transaction.transaction_status}</li>
//                             <li>Phương thức: ${transaction.payment_method}</li>
//                         </ul>
//                     </div>
//                 </details>
//             </td>
//         </tr>`;
//     });

//     return html;
// }

// Hàm chuyển đổi định dạng ngày từ dd/mm/yyyy sang yyyy-mm-dd
function convertDateFormat(dateString) {
    if (!dateString) return ''; // Nếu không có giá trị, trả về chuỗi rỗng
    const [year, month, day] = dateString.split('-');
    return `${day}/${month}/${year}`; // Chuyển đổi thành dd/mm/yyyy
}

// Sự kiện lọc giao dịch
document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault(); // Ngăn chặn form gửi đi

    const transactionId = document.getElementById('transaction-id').value.toLowerCase().trim();
    const transactionDate = convertDateFormat(document.getElementById('transaction-date').value); // Chuyển đổi ngày
    const transactionStatus = document.getElementById('transaction-status').value;
    const paymentMethod = document.getElementById('payment-method').value;

    // Lọc giao dịch dựa trên các điều kiện
    const filteredTransactions = transactions.filter(transaction => {
        return (
            (transactionId === '' || transaction.transaction_id.toLowerCase().includes(transactionId)) &&
            (transactionDate === '' || transaction.transaction_date === transactionDate) &&
            (transactionStatus === '' || transaction.transaction_status === transactionStatus) &&
            (paymentMethod === '' || transaction.payment_method === paymentMethod)
        );
    });

    displayTransactions(filteredTransactions); // Hiển thị giao dịch đã lọc
});

// Xử lý sự kiện cho nút reset
document.getElementById('reset-button').addEventListener('click', function () {
    // Reset các trường lọc
    document.getElementById('transaction-id').value = '';
    document.getElementById('transaction-date').value = '';
    document.getElementById('transaction-status').value = '';
    document.getElementById('payment-method').value = '';

    // Hiển thị lại tất cả giao dịch
    displayTransactions(transactions); // 'transactions' là mảng gốc
});

// Lấy tổng tiền thanh toán vào thông tin chi tiết
document.addEventListener('DOMContentLoaded', function () {
    const detailsElements = document.querySelectorAll('details');

    detailsElements.forEach((details) => {
        details.querySelector('summary').addEventListener('click', function () {
            const row = details.closest('tr'); // Lấy hàng tương ứng
            const totalPayment = row.querySelector('.total-payment').innerHTML; // Lấy nội dung total-payment
            const itemElement = row.querySelector('#total-payment-li'); // Lấy phần tử có id="item"

            if (itemElement) {
                itemElement.innerHTML += totalPayment; // Thêm nội dung total-payment vào item
            }
        });
    });
});