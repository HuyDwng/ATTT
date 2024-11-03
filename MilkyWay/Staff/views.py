from django.shortcuts import render,redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Review 
from django.shortcuts import render, redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Review, Images
from django.shortcuts import get_object_or_404, render  

# Create your views here.

#encrypted and decrypted code
def decrypted_tours():
    tour = Tour.objects.all()
    return [
        {
            'description': t.decrypted_data('description'),
            'name': t.decrypted_data('name'),
            'destination': t.decrypted_data('destination'),
            'price': t.decrypted_data('price'),
        }
        for t in tour
    ]
def get_common_context():
    tours = decrypted_tours()
    return {
        'tour': tours,
        'user': Users.objects.all(),
        'ticket': Tickets.objects.all(),
        'booking': Booking.objects.all(),
        'payment': Payment.objects.all(),
        'review': Review.objects.all(),
    }

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

        return redirect('tour_mng')

    context = {'range': range(1, 5)}
    return render(request, 'tour_management/add_tour.html', context)



def get_tour_edit(request, tour_id):
    # Lấy tour cần chỉnh sửa
    tour = get_object_or_404(Tour, id=tour_id)
    images = Images.objects.filter(tour=tour)
    tour.start_date = tour.start_date.strftime("%Y-%m-%d") if tour.start_date else ""
    tour.end_date = tour.end_date.strftime("%Y-%m-%d") if tour.end_date else ""

    if request.method == 'POST':
        # Cập nhật các thông tin tour từ form
        tour.name = request.POST.get('tour_name')
        tour.start_location = request.POST.get('start_location')
        tour.destination = request.POST.get('destination')
        tour.start_date = request.POST.get('start_date')
        tour.end_date = request.POST.get('end_date')
        tour.price = request.POST.get('tour_price')
        tour.available_seats = request.POST.get('passenger_count')
        tour.remaining_seats = request.POST.get('remaining_count')

        # Thu thập tất cả các mô tả từ form input `description[]`
        descriptions = request.POST.getlist('description[]')  # Sử dụng getlist để lấy tất cả mô tả
        tour.description = '*'.join(descriptions)  # Ghép các mô tả lại với dấu `*` phân cách

        # Lưu lại tour sau khi chỉnh sửa
        tour.save()

        return redirect('tour_mng')  # Chuyển hướng về trang quản lý tour sau khi lưu

    # Nếu là GET, render form với dữ liệu hiện tại

    desc = tour.decrypted_description()
    descriptions = desc.split('*') if tour.description else []
    context = {
        'tour': tour,
        'images': images,
        'descriptions': descriptions,
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