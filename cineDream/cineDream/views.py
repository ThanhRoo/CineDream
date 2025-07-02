from django.shortcuts import render, redirect
from apps.movies.models import Movie
from datetime import date
import json
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def auth_view(request):
    if request.method == "POST":
        if request.path == "/dang-ky":
            # Xử lý đăng ký
            fullname = request.POST.get("fullname", "").strip()
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")
            confirm_password = request.POST.get("confirm_password", "")

            # Kiểm tra dữ liệu
            if password != confirm_password:
                messages.error(request, "Mật khẩu xác nhận không khớp.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Tên đăng nhập đã tồn tại.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email đã được sử dụng.")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=fullname
                )
                user.save()
                messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
                return redirect("/dang-nhap")

        elif request.path == "/dang-nhap":
            # Xử lý đăng nhập
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Đăng nhập thành công!")
                return redirect("/")  # chuyển hướng về trang chủ
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")

    return render(request, "login.html")


def home_page(request):
    return render(request, 'TrangChu.html')


def view_movie(request):
    today = date.today()
    movies = Movie.objects.filter(movie_release__lte=today)          # Phim đang chiếu
    coming_movies = Movie.objects.filter(movie_release__gt=today)    # Phim sắp chiếu

    return render(request, 'TrangChu.html', {
        'movies': movies,
        'coming_movies': coming_movies,
    })