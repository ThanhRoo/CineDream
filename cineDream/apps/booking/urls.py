from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from cineDream import views as main_views
urlpatterns = [  
   path("chon-ghe/<int:schedule_id>/", views.chon_ghe, name="chon_ghe"),
   path("thanh-toan/<int:movie_id>/<int:schedule_id>/", views.thanh_toan, name="thanh_toan"),
]