from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from cineDream import views as main_views
urlpatterns = [  
   path("chon-ghe/<int:schedule_id>/", views.chon_ghe, name="chon_ghe"),
]