from django.db import models
import os
from datetime import datetime
from .utils import encrypt_data, decrypt_data
# Create your models here.
#Tạo bảng, các trường dữ liệu (database)
#ID sẽ được tự động tạo

class Users(models.Model):
    username = models.CharField(max_length=500, blank=False)  # Tên user
    password = models.CharField(max_length=500,blank=False)
    email = models.EmailField(null=True)
    fullname = models.CharField(max_length=200)
    ROLES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='customer')  # Phân quyền
    phone_number = models.IntegerField()
    date_joined = models.DateTimeField(auto_now_add=True, auto_created=True)
    is_actived = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Mã hóa các trường nhạy cảm trước khi lưu
        self.fullname = encrypt_data(self.fullname)
        self.email = encrypt_data(self.email)
        self.password = encrypt_data(self.password)
        self.phone_number = encrypt_data(self.phone_number)


        super().save(*args, **kwargs)

    def load_encrypted(self):
        # Giải mã các trường nhạy cảm khi lấy ra
        self.fullname = decrypt_data(self.fullname)
        self.email = decrypt_data(self.email)
        self.password = decrypt_data(self.password)
        self.phone_number = decrypt_data(self.phone_number)

    def __str__(self):
        return self.username
    

def user_directory_path(instance, filename):
    tour = instance.tour
    name_tour=tour.name
    # Lấy ngày hiện tại
    today = datetime.today()
    date_str = today.strftime("%Y%m%d")  # Định dạng ngày thành YYYYMMDD

    # Đếm số lượng file được tải lên ngày hôm nay
    # Điều này sẽ đếm tất cả các file cùng ngày với username đó
    existing_files_count = Images.objects.filter(
        tour=tour
    ).filter(images__icontains=f"{name_tour}_{date_str}").count()

    # Tạo tên file với username, ngày và số thứ tự
    new_filename = f"{name_tour}_{date_str}_{existing_files_count + 1}{os.path.splitext(filename)[1]}"

    # Trả về đường dẫn đầy đủ cho file
    return os.path.join("", new_filename)

class Tour(models.Model):
    name = models.CharField(max_length=255)  # Tên tour
    description = models.TextField()  # Mô tả tour
    start_location = models.CharField(max_length=255)  # Nơi bắt đầu
    destination = models.CharField(max_length=255)  # Điểm đến
    start_date = models.DateField()  # Ngày khởi hành
    end_date = models.DateField()  # Ngày kết thúc
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Giá tour
    available_seats = models.IntegerField()  # Số lượng chỗ trống
    remaining_seats = models.IntegerField(null=True) # Số lượng chỗ còn lại

    def decrypted_data(self, field_name):
        # Giải mã dữ liệu dựa vào tên trường
        encrypted_value = getattr(self, field_name, None)  # Lấy giá trị từ trường
        if encrypted_value is not None:
            return decrypt_data(encrypted_value)
        return None  # Trả về None nếu trường không tồn tại
    def decrypted_description(self):
        return decrypt_data(self.description)

    def save(self, *args, **kwargs):
        self.description = encrypt_data(self.description)
        self.destination = encrypt_data(self.destination)
        self.start_location = encrypt_data(self.start_location)
        super().save(*args, **kwargs)

    def load_encrypted(self):
        self.description = decrypt_data(self.description)
        self.destination = decrypt_data(self.destination)
        self.start_location = decrypt_data(self.start_location)

    def __str__(self):
        return self.name
   
    def duration_in_days_and_nights(self):
            # Tính khoảng cách giữa end_date và start_date
            duration = self.end_date - self.start_date
            days = duration.days
            nights = days - 1 if days > 0 else 0  # Mỗi đêm là số ngày - 1, ngoại trừ khi chỉ có 1 ngày
            return f"{days} ngày, {nights} đêm"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Người đặt vé (khách hàng)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)  # Tour được đặt
    booking_date = models.DateTimeField(auto_now_add=True)  # Ngày đặt vé
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')  # Trạng thái
    payment_method = models.CharField(max_length=50, blank=True)  # Phương thức thanh toán (nếu có)
    ticket_code = models.CharField(max_length=100, blank=True)  # Mã vé (tạo sau khi thanh toán)

    def __str__(self):
        return f"Booking by {self.user} for {self.tour} with id {self.id}"
    
class Payment(models.Model):
    STATUS_CHOICES = [
        ('successful', 'Successful'),
        ('unpaid', 'Unpaid'),
    ]  
    STATUS_METHOD = [
        ('transfer', 'Transfer'),
        ('cash','Cash'),
        ('credit-card','Credit-card'),
        ('e-wallet','E-wallet')
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)  # Đơn đặt vé
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Số tiền thanh toán
    payment_date = models.DateTimeField(auto_now_add=True)  # Ngày thanh toán
    payment_method = models.CharField(max_length=15, choices=STATUS_METHOD, default="cash")  # Phương thức thanh toán
    payment_state = models.CharField(max_length=15, choices=STATUS_CHOICES, default="unpaid") 
    def __str__(self):
        return f"Payment for {self.booking} on {self.payment_date} with id {self.id}"
    
class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)  # Tour được đánh giá
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Người đánh giá
    star = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Đánh giá từ 1 đến 5 sao
    comment = models.TextField(blank=True)  # Nhận xét (tùy chọn)
    review_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Review by {self.user} for {self.tour} - {self.rating} stars"
    
class Tickets(models.Model):
    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('use', 'Used'),
        ('cancelled', 'Cancelled'),
    ]  
    ticket_code = models.IntegerField()
    issued_date = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    ticket_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')  # Trạng thái vé

    def __str__(self):
        return f"ID ticket {self.id}"

        return url
    
class Images(models.Model):
    tour = models.ForeignKey(Tour,related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    images = models.ImageField(upload_to=user_directory_path, default=None)
    position = models.IntegerField(default=0)

    @property
    def ImageURL(self):
        try:
            url = "/static" + self.images.url
        except:
            url=''
        return url

    def __str__(self):
        return f"{self.tour.name}_image{self.position}" 
    
