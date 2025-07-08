from django.shortcuts import render,get_object_or_404
from collections import defaultdict
from datetime import date, timedelta, datetime
from .models import Schedule
from apps.movies.models import Movie
#  Hàm chuyển tháng tiếng Anh sang số
def convert_month_to_number(month_name):
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12',
    }
    return months.get(month_name)

#  Hàm parse ngày từ nhiều định dạng (YYYY-MM-DD hoặc "July 5, 2025")
def parse_selected_date(raw_date):
    try:
        # format: 2025-07-05
        return date.fromisoformat(raw_date)
    except ValueError:
        try:
            # Format: "July 5, 2025"
            dt = datetime.strptime(raw_date, "%B %d, %Y")
            return dt.date()
        except ValueError:
            return date.today()  # fallback nếu sai định dạng

# View trang chủ
def trang_chu(request):
    return render(request, 'home')

#  View lịch chiếu
def lich_chieu(request):
    today = date.today()
    weekdays = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']

    # Danh sách 7 ngày tiếp theo
    days = []
    for i in range(7):
        d = today + timedelta(days=i)
        days.append({
            'date': d,
            'weekday': weekdays[d.weekday()]
        })

    # Parse ngày từ query (?date=...)
    selected_date_str = request.GET.get('date')
    selected_date = parse_selected_date(selected_date_str) if selected_date_str else today

    # Lấy lịch chiếu trong ngày , kem voi thông tin khoan ngoai movie và room
    schedules = Schedule.objects.select_related('movie', 'room').filter(schedule_date=selected_date)
    movie_dict = defaultdict(list)
    for s in schedules:
        movie_dict[s.movie].append(s)

    # gửi về template
    movies = []
    for movie, sched_list in movie_dict.items():
        movies.append({
            'movie_name': movie.movie_name,
            'poster': movie.movie_image_poster,
            'schedules': sched_list
        })

    return render(request, 'LichChieu.html', {
        'movies': movies,
        'days': days,
        'selected_date': selected_date,
    })

#  View backup hiển thị tất cả lịch chiếu
def lichChieu_1(request):
    schedules = Schedule.objects.all()
    return render(request, 'LichChieu.html', {'Schedules': schedules})

def chon_lich_chieu(request, movie_id):
    today = date.today()
    weekdays = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']

    # Danh sách 7 ngày tiếp theo
    days = []
    for i in range(7):
        d = today + timedelta(days=i)
        days.append({
            'date': d,
            'weekday': weekdays[d.weekday()]
        })

    # Ngày được chọn từ URL (?date=...), mặc định là hôm nay
    selected_date_str = request.GET.get('date')
    selected_date = parse_selected_date(selected_date_str) if selected_date_str else today

    # Lấy movie 
    movie = get_object_or_404(Movie, id=movie_id)

    # Lọc lịch chiếu
    schedules = Schedule.objects.filter(movie=movie, schedule_date=selected_date).select_related('room')

    return render(request, 'ChonLichChieu.html', {
        'movie': movie,
        'schedules': schedules,
        'days': days,
        'selected_date': selected_date,
    })