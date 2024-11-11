//Hiển thị mật khẩu
document.addEventListener('DOMContentLoaded', function() {
    function togglePasswordVisibility() {
        const passwordField = document.getElementById('password');
        const confirmPasswordField = document.getElementById('confirm-password');
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        confirmPasswordField.setAttribute('type', type);
    }

    document.getElementById('checkbox-1').addEventListener('change', function () {
        togglePasswordVisibility();
    });
});

// // Danh sách các group và thành viên trong từng group
//         let groups = {
//             "Group 1": ["Kiệt", "Vỹ"],
//             "Group 2": ["Như", "Quận"],
//             "Group 3": ["Hậu", "Huy"]
//         };

//         // Hàm hiển thị danh sách các group
//         function displayGroups() {
//             const groupList = document.getElementById('group-list');
//             groupList.innerHTML = '';
//             for (let groupName in groups) {
//                 groupList.innerHTML += `
//                     <li class="list-group-item">
//                         <strong>${groupName}</strong>
//                         <button class="btn btn-primary btn-sm ml-3" onclick="viewGroup('${groupName}')">Xem thành viên</button>
//                     </li>`;
//             }
//         }

//         // Hàm hiển thị danh sách thành viên của group được chọn
//         function viewGroup(groupName) {
//             const memberList = document.getElementById('member-list');
//             const currentGroupTitle = document.getElementById('current-group-title');
//             currentGroupTitle.innerText = groupName;
//             memberList.innerHTML = '';
//             groups[groupName].forEach((member, index) => {
//                 memberList.innerHTML += `
//                     <li class="list-group-item d-flex justify-content-between align-items-center">
//                         ${member}
//                         <button class="btn btn-danger btn-sm" onclick="removeMember('${groupName}', ${index})">Xóa</button>
//                     </li>`;
//             });
//         }

//         // Hàm thêm thành viên vào group
//         function addMember() {
//             const newMember = document.getElementById('new-member').value;
//             const currentGroupTitle = document.getElementById('current-group-title').innerText;
//             if (newMember.trim() !== '' && currentGroupTitle) {
//                 groups[currentGroupTitle].push(newMember);
//                 document.getElementById('new-member').value = '';
//                 viewGroup(currentGroupTitle);
//             } else {
//                 alert('Vui lòng nhập tên thành viên và chọn group.');
//             }
//         }

//         // Hàm xóa thành viên khỏi group
//         function removeMember(groupName, index) {
//             groups[groupName].splice(index, 1);
//             viewGroup(groupName);
//         }

//         // Gọi hàm khi trang tải xong
//         document.addEventListener('DOMContentLoaded', function () {
//             displayGroups();
//         });

// // Danh sách user mặc định
//         let users = [
//             { name: 'Vỹ', password: 'password123', role: 'User' },
//             { name: 'Như', password: 'qwerty456', role: 'Admin' },
//             { name: 'Kiệt', password: 'asdfg789', role: 'User' }
//         ];

//         let currentUserIndex = null;

//         // Hiển thị danh sách user
//         function displayUsers() {
//             const userList = document.getElementById('user-list');
//             userList.innerHTML = '';
//             users.forEach((user, index) => {
//                 userList.innerHTML += `
//                     <li class="list-group-item d-flex justify-content-between align-items-center">
//                         ${user.name} (${user.role})
//                         <div>
//                             <button class="btn btn-info btn-sm" onclick="viewUser(${index})">Xem</button>
//                             <button class="btn btn-danger btn-sm" onclick="deleteUser(${index})">Xóa</button>
//                         </div>
//                     </li>`;
//             });
//         }

//         // Xem thông tin user
//         function viewUser(index) {
//             currentUserIndex = index;
//             const user = users[index];
//             document.getElementById('user-info').innerHTML = `
//                 <h5>Thông tin User</h5>
//                 <p>Tên: ${user.name}</p>
//                 <p>Mật khẩu: ${user.password}</p>
//                 <div>
//                     <label for="user-role">Cấp quyền:</label>
//                     <select id="user-role" onchange="changeRole(${index})" class="form-select">
//                         <option value="User" ${user.role === 'User' ? 'selected' : ''}>User</option>
//                         <option value="Admin" ${user.role === 'Admin' ? 'selected' : ''}>Admin</option>
//                     </select>
//                 </div>
//             `;
//         }

//         // Thay đổi quyền của user
//         function changeRole(index) {
//             const newRole = document.getElementById('user-role').value;
//             users[index].role = newRole;
//             displayUsers();
//         }

//         // Xóa user
//         function deleteUser(index) {
//             users.splice(index, 1);
//             displayUsers();
//             document.getElementById('user-info').innerHTML = ''; // Clear user info
//         }

//         document.addEventListener('DOMContentLoaded', () => {
//             displayUsers();
//         });

//         document.addEventListener('DOMContentLoaded', function() {
//             const links = document.querySelectorAll('.sidebar a');

//             // Function to set the active link based on the current URL
//             function setActiveLink() {
//                 const currentURL = window.location.href;

//                 links.forEach(link => {
//                     if (link.href === currentURL) {
//                         link.classList.add('active');
//                     } else {
//                         link.classList.remove('active');
//                     }
//                 });
//             }

//             // Set the active link on page load
//             setActiveLink();

//             // Add click event listener to each link
//             links.forEach(link => {
//                 link.addEventListener('click', function() {
//                     // Remove active class from all links
//                     links.forEach(link => link.classList.remove('active'));

//                     // Add active class to the clicked link
//                     this.classList.add('active');
//                 });
//             });
//         });

//         let tours = [
//         { id: 1, name: "Tour Đà Nẵng", start: "Hà Nội", end: "Đà Nẵng", price: 5000000, duration: 5 },
//         { id: 2, name: "Tour Huế", start: "Hà Nội", end: "Huế", price: 4000000, duration: 4 },
//     ];

//     // Mảng lưu danh sách các tour đã tổ chức
//     let completedTours = [];

//     // Hàm render danh sách tour
//     function renderTours() {
//         const tourList = document.getElementById("tourList");
//         tourList.innerHTML = ""; // Xóa các tour cũ

//         tours.forEach((tour, index) => {
//             const row = `
//                 <tr>
//                     <td>${index + 1}</td>
//                     <td>${tour.name}</td>
//                     <td>${tour.start}</td>
//                     <td>${tour.end}</td>
//                     <td>${tour.price} VND</td>
//                     <td>${tour.duration}</td>
//                     <td>
//                         <button class="btn btn-warning btn-sm" onclick="editTour(${index})">Sửa</button>
//                         <button class="btn btn-danger btn-sm" onclick="deleteTour(${index})">Xóa</button>
//                         <button class="btn btn-success btn-end-tour" data-id="${tour.id}">Kết thúc tour</button>
//                     </td>
//                 </tr>
//             `;
//             tourList.insertAdjacentHTML("beforeend", row);
//         });

//         // Thêm sự kiện cho nút "Kết thúc tour"
//         document.querySelectorAll(".btn-end-tour").forEach(button => {
//             button.addEventListener("click", endTour);
//         });
//     }

//     // Hàm xử lý khi nhấn "Kết thúc tour"
//     function endTour(event) {
//         const tourId = parseInt(event.target.getAttribute("data-id"));
//         const tourIndex = tours.findIndex(t => t.id === tourId);

//         // Di chuyển tour từ danh sách hiện tại sang danh sách đã tổ chức
//         if (tourIndex > -1) {
//             const completedTour = tours.splice(tourIndex, 1)[0]; // Xóa khỏi danh sách hiện tại
//             completedTours.push(completedTour); // Thêm vào danh sách đã tổ chức
//             renderTours(); // Cập nhật lại danh sách
//         }
//     }

//     // Render danh sách tour khi tải trang
//     document.addEventListener("DOMContentLoaded", renderTours);

//     // Hàm render danh sách các tour đã tổ chức
//                 function renderCompletedTours() {
//                     const completedTourList = document.getElementById("completedTourList");
//                     completedTourList.innerHTML = ""; // Xóa các tour cũ
            
//                     completedTours.forEach((tour, index) => {
//                         const row = `
//                             <tr>
//                                 <td>${index + 1}</td>
//                                 <td>${tour.name}</td>
//                                 <td>${tour.start}</td>
//                                 <td>${tour.end}</td>
//                                 <td>${tour.price} VND</td>
//                                 <td>${tour.duration}</td>
//                             </tr>
//                         `;
//                         completedTourList.insertAdjacentHTML("beforeend", row);
//                     });
//                 }
            
//                 // Gọi hàm này khi cần hiển thị danh sách tour đã tổ chức
//                 document.addEventListener("DOMContentLoaded", renderCompletedTours);

//                 let tourData = [];

//         // Hàm hiển thị danh sách tour
//         function displayTours() {
//             const tourList = document.getElementById("tourList");
//             tourList.innerHTML = ""; // Xóa danh sách cũ
//             tourData.forEach((tour, index) => {
//                 const row = `<tr>
//                     <td>${index + 1}</td>
//                     <td>${tour.name}</td>
//                     <td>${tour.start}</td>
//                     <td>${tour.end}</td>
//                     <td>${tour.price} VND</td>
//                     <td>${tour.duration}</td>
//                     <td>
//                         <button class="btn btn-warning btn-sm" onclick="editTour(${index})">Sửa</button>
//                         <button class="btn btn-danger btn-sm" onclick="deleteTour(${index})">Xóa</button>
//                         <button class="btn btn-success btn-end-tour" data-id="1">Kết thúc tour</button>
//                     </td>
//                 </tr>`;
//                 tourList.innerHTML += row;
//             });
//         }

        