from django.shortcuts import render

# Create your views here.
def get_home(request):
    return render(request, 'tour_management/tour_mng.html')
def get_payment(request):
    return render(request,'payment_mng/payment_mng.html')
def get_add_tour(request):
    return render(request,'tour_management/add_tour.html')
def get_tour_edit(request):
    return render(request,'tour_management/tour_edit.html')