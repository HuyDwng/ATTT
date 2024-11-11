function showPersonalInfo() {
    document.getElementById('personalInfo').style.display = 'block';
    document.getElementById('bookedTours').style.display = 'none';
}

function showBookedTours() {
    document.getElementById('personalInfo').style.display = 'none';
    document.getElementById('bookedTours').style.display = 'block';
}

function openModal() {
    document.getElementById('phoneModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('phoneModal').style.display = 'none';
}

function updatePhoneNumber() {
    const newPhoneNumber = document.getElementById('newPhoneNumber').value;
    if (newPhoneNumber) {
        document.querySelector('.info-section .value[data-info="phone"]').innerText = newPhoneNumber;
        closeModal();
    } else {
        alert('Vui lòng nhập số điện thoại mới.');
    }
}