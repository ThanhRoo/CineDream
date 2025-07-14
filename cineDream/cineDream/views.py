from django.shortcuts import render, redirect
from apps.movies.models import Movie
from datetime import date
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import google.generativeai as genai
from django.http import JsonResponse
from apps.schedule.models import Schedule
from collections import defaultdict

# API key 
genai.configure(api_key="AIzaSyDSj9wdMhgpKXF33OhY0SzyDvEOOruRXgo")
model = genai.GenerativeModel("gemini-1.5-flash")

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

@csrf_protect
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "").strip()
            if not user_input:
                return JsonResponse({"error": "Empty message"}, status=400)

            movies = Movie.objects.all()
            schedules = Schedule.objects.select_related("movie", "room").all()

            # Gom lịch chiếu theo movie_id
            schedules_by_movie = defaultdict(list)
            for s in schedules:
                schedules_by_movie[s.movie_id].append(s)

            # Tạo dữ liệu mô tả phim + lịch chiếu
            movie_data = ""
            for m in movies:
                showtimes = schedules_by_movie.get(m.id, [])
                if showtimes:
                    lich_chieu = ", ".join([
                        f"{s.schedule_date.strftime('%d/%m')} lúc {s.schedule_start.strftime('%H:%M')} (phòng {s.room.room_name})"
                        for s in showtimes
                    ])
                else:
                    lich_chieu = "Không có lịch chiếu"

                movie_data += (
                    f'- Tên phim: "{m.movie_name}" | Thể loại: {m.movie_genres} | '
                    f'- Mô tả: {m.movie_description[:100]}... | '
                    f'- Độ dài , thời lượng :{m.movie_lenght.strftime("%H:%M")} | '
                    f'Ngày phát hành , hoặc khởi chiếu: {m.movie_release.strftime("%d/%m/%Y")} | Lịch chiếu: {lich_chieu}\n'
                )

            # Tạo prompt cho Gemini
            prompt = f"""
                    Bạn là trợ lý chatbot của rạp chiếu phim CineDream. Dưới đây là danh sách các bộ phim cùng thể loại, ngày phát hành và lịch chiếu cụ thể.
                    Địa điểm rạp : CineDream ở 250 Nguyễn Văn Linh, Quận Hải Châu , Đà Nẵng.
                    Khách hàng muốn đặt vé : Bước 1: nhấn vào nút đặt vé , Bước 2 Chọn suất chiếu , Bước 3 : Chọn ghế , Cuối cùng là thanh toán.
                    
                    {movie_data}

                    Khách hàng hỏi: "{user_input}"

                    Dựa vào thông tin trên, hãy trả lời ngắn gọn, đúng trọng tâm và dễ hiểu.Lịch chiếu không nói những lịch chiếu đã qua.Nếu không có thông tin phù hợp, hãy lên mạng tìm kiếm và trả lời khách hàng một cách lịch sự. Tránh trả lời quá dài dòng hoặc không liên quan."
                """

            # Gửi đến Gemini
            response = model.generate_content(prompt)
            reply = response.text.strip()

            return JsonResponse({"reply": reply})

        except Exception as e:
            import traceback
            print(traceback.format_exc())  # log lỗi ra console
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)