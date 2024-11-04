tài khoản admin django: admin
mật khẩu: 123
khi đăng nhập bằng gaio diện đăng nhập vẫn chưa vô được trang chủ do chưa gắn đường dẫn

Đề tài nhóm chúng em chia ra làm 3 phân quyền User, Staff, Admin
Do mỗi phân quyền do 1 nhóm phụ trách nên các chức năng, thanh toán và mã hóa vẫn đang cập nhật và sửa lỗi. Đã lấy được và cập nhận
dữ liệu, hình ảnh trên giao diện
từ database
các giao diện chưa có gắn đường dẫn liên kết với nhau nhưng vẫn có thể truy cập trực tiếp bằng các đường dẫn URL:
+ Admin:
    giao diện admin: địa_chỉ_localhost/tour-list
+ Staff: đã gắn link nên có thể truy cập tất cả chức năng
    giao diện staff: địa_chỉ_localhost/staff
+ User:
    các tour: địa_chỉ_localhost/tour 
    chi tiết tour: địa_chỉ_localhost/tour_detail   
    xác nhận thanh toán: địa_chỉ_localhost/confirm-payment   
    địa_chỉ_localhost/search_tours     
    Trang chủ: địa_chỉ_localhost  
+ Log-In: 
    đăng nhập: địa_chỉ_localhost/log-in/login
    đăng kí: địa_chỉ_localhost/log-in/register

