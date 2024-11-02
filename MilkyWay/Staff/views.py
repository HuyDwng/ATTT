from django.shortcuts import render,redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Review 
from django.shortcuts import render, redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Review, Images
from django.shortcuts import get_object_or_404, render  

# Create your views here.
def get_home(request):  
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'tour_management/tour_mng.html', context)
def get_payment(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request,'payment_mng/payment_mng.html', context)



def get_add_tour(request):
    if request.method == 'POST':
        # Nhận thông tin tour từ form
        user_tour = request.POST.get('tour_code')
        name = request.POST.get('tour_name')
        start_location = request.POST.get('start_location')
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        price = request.POST.get('tour_price')
        available_seats = request.POST.get('passenger_count')
        remaining_seats = available_seats

        # Thu thập mô tả địa điểm từ các trường itinerary_0, itinerary_1, ...
        descriptions = []
        for key in request.POST:
            if key.startswith('itinerary_'):
                descriptions.append(request.POST.get(key))
        
        description = '*'.join(descriptions)  # Ghép các mô tả lại với dấu `*` phân cách

        # Lưu thông tin Tour
        tour = Tour(
            user_tour=user_tour,
            name=name,
            description=description,
            start_location=start_location,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            price=price,
            available_seats=available_seats,
            remaining_seats=remaining_seats,
        )
        tour.save()

        # Lưu ảnh
        images = request.FILES.getlist('tour_image')
        for idx, image in enumerate(images):
            Images.objects.create(tour=tour, images=image, position=idx + 1)

        return redirect('tour_management')

    context = {'range': range(1, 5)}
    return render(request, 'tour_management/add_tour.html', context)



def get_tour_edit(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    images = Images.objects.filter(tour=tour)  # Lấy các ảnh thuộc tour này
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    tour.start_date = tour.start_date.strftime("%Y-%m-%d") if tour.start_date else ""
    tour.end_date = tour.end_date.strftime("%Y-%m-%d") if tour.end_date else ""
   
    # Tách description thành danh sách, nếu description không rỗng
    descriptions = tour.description.split('*') if tour.description else []

    # Cập nhật context để bao gồm danh sách ảnh
    context = {
        'range': range(1, 5),
        'tour': tour,
        'images': images,  # Thêm danh sách ảnh vào context
        'user': user,
        'ticket': ticket,
        'booking': booking,
        'payment': payment,
        'review': review,
        'descriptions': descriptions,  # Thêm danh sách mô tả vào context
    }
    return render(request, 'tour_management/tour_edit.html', context)



def delete_image(request, image_id):
    image = get_object_or_404(Images, id=image_id)  # Tìm ảnh theo ID
    if request.method == 'POST':
        image.delete()  # Xóa ảnh khỏi database
        return redirect('tour_edit', tour_id=image.tour.id)  # Điều hướng trở lại trang chỉnh sửa tour

def add_images(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, id=tour_id)
        images = request.FILES.getlist('tour_images')  # Nhận danh sách file hình ảnh
        for img in images:
            Images.objects.create(tour=tour, images=img)  # Tạo đối tượng hình ảnh
            
        return redirect('tour_edit', tour_id=tour_id)  # Điều hướng lại trang chỉnh sửa tour
    
def change_image(request, image_id):
    image = get_object_or_404(Images, id=image_id)
    if request.method == 'POST':
        new_image = request.FILES.get('new_image')  # Nhận hình ảnh mới
        if new_image:
            image.images = new_image  # Thay đổi hình ảnh
            image.save()  # Lưu thay đổi
    return redirect('tour_edit', tour_id=image.tour.id)  # Điều hướng lại trang chỉnh sửa tour

def get_revenue_statistics(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request,'revenue_statistics/revenue_statistics.html',context)