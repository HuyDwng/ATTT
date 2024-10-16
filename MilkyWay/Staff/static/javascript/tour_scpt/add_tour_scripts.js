let sectionCount = 0; // Đếm số lượng khu vực

// Hàm để thêm một khu vực mới
function addTourSection() {
    sectionCount++;

    const newSection = document.createElement('div');
    newSection.classList.add('form-section');
    newSection.setAttribute('id', `tour_section_${sectionCount}`);

    // Nội dung khu vực mới
    newSection.innerHTML = `
        <h2 class="form-section-title">Khu Vực ${sectionCount}</h2>

        <label for="tour_image_${sectionCount}">Hình Ảnh Khu Vực ${sectionCount}:</label>
        <input type="file" id="tour_image_${sectionCount}" name="tour_image_${sectionCount}" accept="image/*" required>
        <button type="button" class="remove-image-btn">Xóa Hình Ảnh</button>
        <br>

        <label for="itinerary_${sectionCount}">Mô Tả Khu Vực ${sectionCount}:</label>
        <textarea id="itinerary_${sectionCount}" name="itinerary_${sectionCount}" required></textarea>

        <button type="button" class="remove-section-btn">Xóa Khu Vực</button>
    `;

    const tourSectionsContainer = document.getElementById('tour_sections_container');
    tourSectionsContainer.appendChild(newSection);

    // Gắn sự kiện xóa hình ảnh
    newSection.querySelector('.remove-image-btn').addEventListener('click', function () {
        removeImage(newSection);
    });

    // Gắn sự kiện xóa khu vực
    newSection.querySelector('.remove-section-btn').addEventListener('click', function () {
        removeTourSection(newSection);
    });
}

// Hàm xóa hình ảnh
function removeImage(section) {
    const imageInput = section.querySelector('input[type="file"]');
    imageInput.value = ''; // Xóa giá trị của trường input file
}

// Hàm xóa khu vực
function removeTourSection(section) {
    section.remove(); // Xóa khu vực khỏi trang
}

// Gắn sự kiện click vào nút "Thêm Khu Vực"
document.getElementById('add_section_btn').addEventListener('click', addTourSection);
