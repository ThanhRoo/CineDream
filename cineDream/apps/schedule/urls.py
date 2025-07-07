from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from cineDream import views as main_views
urlpatterns = [  
   path("", views.lich_chieu, name="lich_chieu"),
   path("chon-lich-chieu/<int:movie_id>/", views.chon_lich_chieu, name="chon_lich_chieu"),
]