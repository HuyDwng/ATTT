let sectionCount = 0; // Đếm số lượng khu vực

// Hàm để thêm một khu vực mới
function addTourSection() {
    sectionCount++;

    const newSection = document.createElement('div');//section thật ra là các đối tượng div
    newSection.classList.add('form-section');//thiết lập tên class cho div
    newSection.setAttribute('id', `tour_section_${sectionCount}`);//thiết lập id cho div

    // Nội dung khu vực mới
    newSection.innerHTML = `
        <h2 class="form-section-title">Địa Điểm ${sectionCount}</h2>

        <label for="tour_image_${sectionCount}">Hình Ảnh Địa Điểm ${sectionCount}:</label>
        <input type="file" id="tour_image_${sectionCount}" name="tour_image_${sectionCount}" accept="image/*" required>
        <button type="button" class="remove-image-btn">Xóa Hình Ảnh</button>
        <br>

        <label for="itinerary_${sectionCount}">Mô Tả Địa Điểm ${sectionCount}:</label>
        <textarea id="itinerary_${sectionCount}" name="itinerary_${sectionCount}" required></textarea>

        <button type="button" class="remove-section-btn">Xóa Địa Điểm</button>
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
    const sectionId = parseInt(section.id.split('_')[2]); // Lấy số thứ tự của section bị xóa

    section.remove(); // Xóa khu vực khỏi trang

    // Cập nhật lại các section có id lớn hơn
    updateSectionsAfterRemoval(sectionId);
}

// Hàm cập nhật lại thứ tự của các section sau khi xóa một section
function updateSectionsAfterRemoval(removedSectionId) {
    const tourSectionsContainer = document.getElementById('tour_sections_container');
    const remainingSections = tourSectionsContainer.querySelectorAll('.form-section');

    remainingSections.forEach((section, index) => { //index được khởi tạo bằng 0
        //đánh số lại bắt đầu từ index=1 đến hết(index lúc mới khởi tạo có giá trị là 0)
        const currentSectionId = index + 1;

        // Cập nhật id và tiêu đề cho section
        section.setAttribute('id', `tour_section_${currentSectionId}`);
        section.querySelector('.form-section-title').textContent = `Địa điểm ${currentSectionId}`;
        section.querySelector('label[for^="tour_image"]').setAttribute('for', `tour_image_${currentSectionId}`);
        section.querySelector('input[type="file"]').setAttribute('id', `tour_image_${currentSectionId}`);
        section.querySelector('input[type="file"]').setAttribute('name', `tour_image_${currentSectionId}`);
        section.querySelector('label[for^="itinerary"]').setAttribute('for', `itinerary_${currentSectionId}`);
        section.querySelector('textarea').setAttribute('id', `itinerary_${currentSectionId}`);
        section.querySelector('textarea').setAttribute('name', `itinerary_${currentSectionId}`);
    });

    // Cập nhật lại giá trị của sectionCount
    sectionCount = remainingSections.length;
}

// Gắn sự kiện click vào nút "Thêm Khu Vực"
document.getElementById('add_section_btn').addEventListener('click', addTourSection);
