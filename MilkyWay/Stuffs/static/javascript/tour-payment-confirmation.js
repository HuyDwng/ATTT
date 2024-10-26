/*Lưu thông tin liên hệ*/
let currentName = ""; // Biến lưu trữ tên hiện tại
let currentEmail = "";
let currentPhone = "";
let currentAddress = "";
let titleForm = document.getElementById("contact-info-header").textContent;

function setupSaveButton() {
    const saveButton = document.getElementById("save-button");

    // Gán sự kiện cho nút "Lưu"
    saveButton.onclick = function() {
        const nameInput = document.getElementById("name");
        const emailInput = document.getElementById("email");
        const phoneInput = document.getElementById("sdt");
        const addressInput = document.getElementById("address");

        const name = nameInput.value.trim(); // Lấy giá trị từ ô nhập liệu và loại bỏ khoảng trắng
        const email = emailInput.value.trim();
        const phone = phoneInput.value.trim();
        const address = addressInput.value.trim();

        if (name && email && phone && address) {
            // Cập nhật tên hiện tại
            currentName = name;            
            currentEmail = email;
            currentPhone = phone;
            currentAddress = address;

            // Đổi tiêu đề về tên đã lưu
            document.getElementById("contact-info-header").innerText = currentName;

            // Hiển thị thông tin đã lưu
            document.getElementById("display-email").innerText = currentEmail;
            document.getElementById("display-phone").innerText = currentPhone;
            document.getElementById("display-address").innerText = currentAddress;

            // Ẩn form và đổi chữ nút
            document.getElementById("contact-form").classList.remove("visible"); // Ẩn form
            document.getElementById("contact-info-display").classList.remove("hidden"); // Hiện thông tin đã lưu
            console.log("Form hidden");

            // Đổi chữ cho nút và hiển thị nút chỉnh sửa
            this.classList.add("hidden"); // Ẩn nút "Lưu"
            document.getElementById("edit-button").classList.remove("hidden"); // Hiện nút "Chỉnh sửa chi tiết"
        } else {
            alert("Vui lòng nhập họ tên trước khi lưu.");
        }
    };

    // Gán sự kiện cho nút "Chỉnh sửa chi tiết"
    document.getElementById("edit-button").onclick = function() {
        const nameInput = document.getElementById("name");
        const emailInput = document.getElementById("email");
        const phoneInput = document.getElementById("sdt");
        const addressInput = document.getElementById("address");

        // Đặt giá trị ô nhập liệu bằng thông tin hiện tại
        nameInput.value = currentName;
        emailInput.value = currentEmail;
        phoneInput.value = currentPhone;
        addressInput.value = currentAddress;

        // Hiện form và ẩn thông tin liên lạc
        document.getElementById("contact-form").classList.add("visible"); // Hiện form

        document.getElementById("contact-info-display").classList.add("hidden"); // Ẩn thông tin đã lưu
        // Đổi chữ nút và ẩn nút "Chỉnh sửa chi tiết"
        document.getElementById("contact-info-header").innerText =titleForm ;
        saveButton.classList.remove("hidden");
        this.classList.add("hidden");
    };
}

// Gọi hàm thiết lập nút "Lưu" khi trang tải
setupSaveButton();

/* Lưu thông tin khách  */
let currentGuestName = ""; // Biến lưu trữ tên khách hiện tại
let currentGuestEmail = ""; // Biến lưu trữ email khách hiện tại
let currentGuestPhone = ""; // Biến lưu trữ số điện thoại khách hiện tại
let currentGuestAddress = ""; // Biến lưu trữ địa chỉ khách hiện tại
let currentGuestSalutation = ""; // Biến lưu trữ danh xưng khách hiện tại
let titleForm2 = document.getElementById("guest-info-header").textContent;

function setupSaveButton2() {
    const saveButton = document.getElementById("g-save-button");

    // Gán sự kiện cho nút "Lưu"
    saveButton.onclick = function() {
        const salutationInput = document.getElementById("salutation");
        const nameInput = document.getElementById("guest-name");
        const emailInput = document.getElementById("guest-email");
        const phoneInput = document.getElementById("guest-phone");
        const addressInput = document.getElementById("guest-address");

        const salutation = salutationInput.value; // Lấy giá trị danh xưng
        const name = nameInput.value.trim(); // Lấy giá trị từ ô nhập liệu và loại bỏ khoảng trắng
        const email = emailInput.value.trim();
        const phone = phoneInput.value.trim();
        const address = addressInput.value.trim();

        if (salutation && name && email && phone && address) {
            // Cập nhật thông tin khách hiện tại
            currentGuestSalutation = salutation; // Lưu danh xưng
            currentGuestName = name;            
            currentGuestEmail = email;
            currentGuestPhone = phone;
            currentGuestAddress = address;

            // Đổi tiêu đề về tên đã lưu
            document.getElementById("guest-info-header").innerText = currentGuestSalutation + " " + currentGuestName;

            // Hiển thị thông tin đã lưu
            document.getElementById("g-display-email").innerText = currentGuestEmail;
            document.getElementById("g-display-phone").innerText = currentGuestPhone;
            document.getElementById("g-display-address").innerText = currentGuestAddress;

            // Ẩn form và đổi chữ nút
            document.getElementById("guest-inform-form").classList.remove("visible"); // Ẩn form
            document.getElementById("guest-info-display").classList.remove("hidden"); // Hiện thông tin đã lưu

            // Đổi chữ cho nút và hiển thị nút chỉnh sửa
            this.classList.add("hidden"); // Ẩn nút "Lưu"
            document.getElementById("g-edit-button").classList.remove("hidden"); // Hiện nút "Chỉnh sửa chi tiết"
        } else {
            alert("Vui lòng nhập đầy đủ thông tin trước khi lưu.");
        }
    };

    // Gán sự kiện cho nút "Chỉnh sửa chi tiết"
    document.getElementById("g-edit-button").onclick = function() {
        const nameInput = document.getElementById("guest-name");
        const emailInput = document.getElementById("guest-email");
        const phoneInput = document.getElementById("guest-phone");
        const addressInput = document.getElementById("guest-address");
        const salutationInput = document.getElementById("salutation");

        // Đặt giá trị ô nhập liệu bằng thông tin hiện tại
        salutationInput.value = currentGuestSalutation; // Đặt danh xưng
        nameInput.value = currentGuestName;
        emailInput.value = currentGuestEmail;
        phoneInput.value = currentGuestPhone;
        addressInput.value = currentGuestAddress;

        // Hiện form và ẩn thông tin liên lạc
        document.getElementById("guest-inform-form").classList.add("visible"); // Hiện form
        document.getElementById("guest-info-display").classList.add("hidden"); // Ẩn thông tin đã lưu

        // Đổi tiêu đề và hiển thị nút "Lưu"
        document.getElementById("guest-info-header").innerText = titleForm2;
        saveButton.classList.remove("hidden");
        this.classList.add("hidden");
    };
}
// Gọi hàm thiết lập nút "Lưu" khi trang tải
setupSaveButton2();





/* Chuyển hướng qua trang thanh toán */
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('confirmation-popup').classList.add('disapear');
    document.getElementById('error-container').style.display = 'none';
});
// Xử lý khi kiểm tra thông tin có được điền đầy đủ hay chưa
document.getElementById('pay-button').addEventListener('click', function(event) {
    // Lấy tất cả các ô input bắt buộc
    const requiredInputs = document.querySelectorAll('input.required');
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

    // Kiểm tra tính hợp lệ của cả hai form
    var isFormValid = document.getElementById('contact-form').checkValidity() && 
                      document.getElementById('guest-inform-form').checkValidity();

    if (!allFilled || !isFormValid) {
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


/* Lựa chọn khách hay đặt hộ */
// Lấy các phần tử cần thao tác
const customerRadio = document.querySelector('input[value="khach"]');
const contactForm = document.getElementById('contact-form');
const guestForm = document.getElementById('guest-inform-form');
const saveButton = document.getElementById('save-button');
const gSaveButton = document.getElementById('g-save-button');

// JSON object to store customer information
let customerInfo = {};

// Function to copy contact info to guest info
function copyContactInfo() {
    // Lấy giá trị từ form liên hệ
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('sdt').value;
    const address = document.getElementById('address').value;

    // Điền thông tin liên hệ vào form khách, trừ danh xưng
    document.getElementById('guest-name').value = name;
    document.getElementById('guest-email').value = email;
    document.getElementById('guest-phone').value = phone;
    document.getElementById('guest-address').value = address;

    // Lưu thông tin vào đối tượng JSON
    customerInfo = {
        name: name,
        email: email,
        phone: phone,
        address: address,
        salutation: document.getElementById('salutation').value // Danh xưng sẽ được chọn riêng
    };

    console.log("Customer Info Saved: ", customerInfo);
}

// Function to save contact info
function saveContactInfo() {
    const contactFormInputs = contactForm.querySelectorAll('input');
    let isValid = true;
    
    // Check if all inputs are filled
    contactFormInputs.forEach(input => {
        if (!input.value) {
            isValid = false;
        }
    });

    if (isValid) {
        saveButton.classList.add('hidden'); // Ẩn nút Lưu sau khi lưu thông tin
        console.log("Contact information saved.");
    } else {
        console.log("Please fill all contact information.");
    }
}

// Function to save guest info
function saveGuestInfo() {
    const guestFormInputs = guestForm.querySelectorAll('input');
    let isValid = true;
    
    // Check if all inputs are filled
    guestFormInputs.forEach(input => {
        if (!input.value) {
            isValid = false;
        }
    });

    if (isValid) {
        gSaveButton.classList.add('hidden'); // Ẩn nút Lưu sau khi lưu thông tin
        console.log("Guest information saved.");
    } else {
        console.log("Please fill all guest information.");
    }
}

// Event listener when user selects "Tôi là khách"
customerRadio.addEventListener('click', function() {
    copyContactInfo();
});

// Event listeners for saving forms
saveButton.addEventListener('click', saveContactInfo);
gSaveButton.addEventListener('click', saveGuestInfo);
