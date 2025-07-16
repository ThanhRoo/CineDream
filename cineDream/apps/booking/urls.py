from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from cineDream import views as main_views
urlpatterns = [  
   path("chon-ghe/<int:schedule_id>/", views.chon_ghe, name="chon_ghe"),
   path("dat-ve/thanh-toan/<uuid:token>/", views.thanh_toan, name="thanh_toan"),
   path('thanh-toan-momo/<int:movie_id>/', views.thanh_toan_momo, name='thanh_toan_momo'),
   path('momo/return/', views.momo_return, name='momo_return'),
   path('momo/ipn/', views.momo_ipn, name='momo_ipn'),
]