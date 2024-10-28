from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(Tour)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(Tickets)
admin.site.register(Images)