// Lấy dữ liệu===================================================================================

const filePath = 'revenue_statistics_data.json';

let revenue = [];

// Fetch the data from the JSON file
fetch(filePath)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        revenue = data;
        displayRevenue(revenue);
    })
    .catch(error => console.error('There has been a problem with your fetch operation:', error));

// Hàm hiển thị doanh thu
function displayRevenue(revenue) {
    const htmlContent = generateHTMLTable(revenue);
    document.querySelector('tbody').innerHTML = htmlContent; // Thêm HTML vào tbody
}


// Hàm tạo HTML
function generateHTMLTable(revenue) {
    let html = '';

    revenue.forEach(revenue => {
        html += `
       <tr>
            <td>${revenue.tour_id_data}</td>
            <td>${revenue.tour_name_data}</td>
            <td>${revenue.books_value}</td>
            <td>${revenue.total_revenue * revenue.books_value}</td>
            
        </tr>`;
    });

    return html;
}


// Sự kiện lọc giao dịch
document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault(); // Ngăn chặn form gửi đi
    const tourId = document.getElementById('tour-id').value.toLowerCase().trim();
    const tourName = document.getElementById('tour-name').value.toLowerCase().trim();
    const booksValue = document.getElementById('books-slider').value;
    const totalRevenue = document.getElementById('revenue-selects').value;
    // const 
    // Lọc giao dịch dựa trên các điều kiện

    // revenue.forEach(revenue => {
    //     if (revenue.books_value < booksValue) document.getElementById('tour-id').value++;
    // });
    // displayRevenue(filteredRevenue);

    let filteredRevenue = revenue.filter(revenue => {
        return (
            (tourId === '' || revenue.tour_id_data.toLowerCase().trim().includes(tourId)) &&
            (tourName === '' || revenue.tour_name_data.toLowerCase().trim().includes(tourName)) &&
            (booksValue === 0 || revenue.books_value < booksValue)
        );
    });

    filteredRevenue = filterDataByRevenue(totalRevenue, filteredRevenue);

    displayRevenue(filteredRevenue); // Hiển thị thống kê đã lọc

});
// Xử lý sự kiện cho nút reset
document.getElementById('reset-button').addEventListener('click', function () {
    // Reset các trường lọc
    document.getElementById('tour-id').value = '';
    document.getElementById('tour-name').value = '';
    document.getElementById('books-slider').value = 0;
    document.getElementById('revenue-selects').value = 'op1'

    // Hiển thị lại tất cả thống kê
    displayRevenue(revenue); // 'revenue' là mảng gốc
});

// Hàm lọc dữ liệu theo doanh thu
function filterDataByRevenue(range, revenue) {
    let filteredData;
    switch (range) {
        case 'op1':
            filteredData = revenue.filter(revenue => (revenue.total_revenue * revenue.books_value) < 50000000)
            break;
        case 'op2':
            filteredData = revenue.filter(revenue => (revenue.total_revenue * revenue.books_value) >= 50000000 && (revenue.total_revenue * revenue.books_value) < 100000000);
            break;
        case 'op3':
            filteredData = revenue.filter(revenue => (revenue.total_revenue * revenue.books_value) >= 100000000 && (revenue.total_revenue * revenue.books_value) <= 200000000);
            break;
        case 'op4':
            filteredData = revenue.filter(revenue => (revenue.total_revenue * revenue.books_value) > 200000000);
            break;

    }

    return filteredData;
}
// =======================thay đổi giá trị book slider =======================
const slider = document.getElementById('books-slider');
const sliderValue = document.getElementById('slider-value');

// Hàm để cập nhật giá trị khi người dùng kéo slider
function updateSliderValue() {
    const value = slider.value; // Lấy giá trị hiện tại của slider
    sliderValue.textContent = (value);
}

// Lắng nghe sự kiện input để cập nhật giá trị liên tục
slider.addEventListener('input', updateSliderValue);

// Gọi hàm để hiển thị giá trị ban đầu
updateSliderValue();

