let sectionCount = 0; // Đếm số lượng khu vực

// Hàm để thêm một khu vực mới
function addTourSection() {
    if (sectionCount <= 3) { // Giới hạn tối đa 3 địa điểm
        sectionCount++;

        const newSection = document.createElement('div');
        newSection.classList.add('form-section');
        newSection.setAttribute('id', `tour_section_${sectionCount}`);

        newSection.innerHTML = `
            <h2 class="form-section-title">Địa Điểm ${sectionCount}</h2>
            <div class="image-drop-zone" id="drop_zone_${sectionCount}">
                Kéo thả hình ảnh vào đây hoặc chọn hình ảnh
            </div>
            <input type="file" id="tour_image_${sectionCount}" name="tour_image_${sectionCount}" accept="image/*" style="display:none;" required>
            <img id="image_preview_${sectionCount}" class="image-preview" style="display:none;">
            <button type="button" class="remove-image-btn" style="display:none;">Xóa Hình Ảnh</button><br>
            <label for="itinerary_${sectionCount}">Mô Tả Địa Điểm ${sectionCount}:</label>
            <textarea id="itinerary_${sectionCount}" name="itinerary_${sectionCount}" required></textarea>
            <button type="button" class="remove-section-btn">Xóa Địa Điểm</button>
        `;

        const tourSectionsContainer = document.getElementById('tour_sections_container');
        tourSectionsContainer.appendChild(newSection);

        // Gắn sự kiện drag-and-drop và chọn hình ảnh
        const dropZone = newSection.querySelector(`#drop_zone_${sectionCount}`);
        const fileInput = newSection.querySelector(`#tour_image_${sectionCount}`);
        const imagePreview = newSection.querySelector(`#image_preview_${sectionCount}`);
        const removeImageBtn = newSection.querySelector('.remove-image-btn');

        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (event) => event.preventDefault());
        dropZone.addEventListener('drop', (event) => {
            event.preventDefault();
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files; // Gán files vào input
                handleImageUpload(fileInput, imagePreview, removeImageBtn, dropZone);
            }
        });

        fileInput.addEventListener('change', () => {
            handleImageUpload(fileInput, imagePreview, removeImageBtn, dropZone);
        });

        removeImageBtn.addEventListener('click', () => {
            fileInput.value = '';
            imagePreview.src = '';
            imagePreview.style.display = 'none';
            removeImageBtn.style.display = 'none';
            dropZone.style.display = 'flex';
        });

        // Gắn sự kiện xóa khu vực
        newSection.querySelector('.remove-section-btn').addEventListener('click', function () {
            removeTourSection(newSection);
        });
    }
}

// Hàm xử lý khi người dùng chọn hoặc kéo thả hình ảnh
function handleImageUpload(fileInput, imagePreview, removeImageBtn, dropZone) {
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            removeImageBtn.style.display = 'inline-block';
            dropZone.style.display = 'none'; // Ẩn khung drag-and-drop khi có hình ảnh
        };
        reader.readAsDataURL(file);
    }
}

// Hàm xóa khu vực
function removeTourSection(section) {
    section.remove();
    sectionCount--;

    const tourSectionsContainer = document.getElementById('tour_sections_container');
    const remainingSections = tourSectionsContainer.querySelectorAll('.form-section');

    // Cập nhật lại số thứ tự cho các section còn lại
    remainingSections.forEach((section, index) => {
        const currentSectionId = index + 1; // Đánh số từ 1 trở đi

        // Cập nhật id và tiêu đề cho section
        section.setAttribute('id', `tour_section_${currentSectionId}`);
        section.querySelector('.form-section-title').textContent = `Địa điểm ${currentSectionId}`;

        // Cập nhật lại id và for cho input, textarea và nhãn
        const fileInput = section.querySelector('input[type="file"]');
        const itineraryLabel = section.querySelector('label[for^="itinerary"]');
        const itineraryTextarea = section.querySelector('textarea');

        section.querySelector('.image-drop-zone').setAttribute('id', `drop_zone_${currentSectionId}`);

        fileInput.setAttribute('id', `tour_image_${currentSectionId}`);
        fileInput.setAttribute('name', `tour_image_${currentSectionId}`);

        itineraryLabel.setAttribute('for', `itinerary_${currentSectionId}`);
        itineraryTextarea.setAttribute('id', `itinerary_${currentSectionId}`);
        itineraryTextarea.setAttribute('name', `itinerary_${currentSectionId}`);
    });
}


// Gắn sự kiện click vào nút "Thêm Khu Vực"
document.getElementById('add_section_btn').addEventListener('click', addTourSection);