from django.contrib import admin
from django.urls import include, path
from Staff import views as Staff 

#Đường dẫn đến các website path("các từ nằm trước đường dẫn để vào website đó")
#VD: để truy cập 127.0.0.1:8000/HomePage ==>  path("HomePage/", include("HomePage.urls"))
urlpatterns = [
    path("log-in/", include("Log-In.urls")),
    path("", include("Stuffs.urls")),
    path("admin/", admin.site.urls),
    path("staff/", include("Staff.urls")),
    path("management/", include("Management.urls"))
]