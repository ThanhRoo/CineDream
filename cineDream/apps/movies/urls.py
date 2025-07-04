from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from cineDream import views as main_views
urlpatterns = [  
    path("<int:phim_id>/chi-tiet/", views.chiTietPhim, name="chi_tiet_phim"),
    path("danh-sach/",views.danhSachPhim , name = "danh_sach_phim"),
]