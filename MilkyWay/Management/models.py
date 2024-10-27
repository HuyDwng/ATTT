from django.db import models

# Create your models here.
#Tạo bảng, các trường dữ liệu (database)
#ID sẽ được tự động tạo

class Users(models.Model):
    username = models.CharField(max_length=255, blank=False)  # Tên user
    password = models.IntegerField(blank=False)
    email = models.EmailField(null=True)
    fullname = models.CharField(max_length=200)
    ROLES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='customer')  # Phân quyền
    phone_number = models.IntegerField()  # Số điện thoại
    date_joined = models.DateTimeField(auto_now_add=True)
    is_actived = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class Tour(models.Model):
    name = models.CharField(max_length=255)  # Tên tour
    description = models.TextField()  # Mô tả tour
    start_location = models.CharField(max_length=255)  # Nơi bắt đầu
    destination = models.CharField(max_length=255)  # Điểm đến
    start_date = models.DateField()  # Ngày khởi hành
    end_date = models.DateField()  # Ngày kết thúc
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá tour
    available_seats = models.IntegerField()  # Số lượng chỗ trống
    images = models.ImageField(default=None)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.images.url
        except:
            url=''
        return url


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
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)  # Đơn đặt vé
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Số tiền thanh toán
    payment_date = models.DateTimeField(auto_now_add=True)  # Ngày thanh toán
    payment_method = models.CharField(max_length=50)  # Phương thức thanh toán

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
    quanlity = models.IntegerField(default=0)
    ticket_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')  # Trạng thái vé

    def __str__(self):
        return f"ID ticket {self.id}"
