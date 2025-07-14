"""
URL configuration for cineDream project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path 
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.view_movie, name='home'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path("dang-nhap", views.auth_view , name ='login'),
    path("dang-ky", views.auth_view),
    path("phim/",include ("apps.movies.urls")),
    path("lich-chieu/", include("apps.schedule.urls")),
    path("dat-ve/", include("apps.booking.urls")),
    path("api/chatbot/", views.chatbot_response, name="chatbot_api"),
]
