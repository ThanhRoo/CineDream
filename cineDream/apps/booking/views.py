from django.shortcuts import render, get_object_or_404
from apps.schedule.models import Schedule
from apps.seats.models import Seats
from apps.booking.models import Booking

def chon_ghe(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    movie = schedule.movie
    room = schedule.room

    all_seats = Seats.objects.filter(room=room)
    booked_seat_ids = Booking.objects.filter(schedule=schedule).values_list('seat_id', flat=True)

    # Tạo cấu trúc dữ liệu để hiển thị theo hàng ghế
    seat_rows = {}
    for seat in all_seats:
        css_class = get_css_class(seat.seat_type)
        if seat.id in booked_seat_ids:
            css_class = "gray"  # Ghế đã đặt

        seat_code = f"{seat.row_label}{seat.number}"
        seat_data = {
            'code': seat_code,
            'css_class': css_class
        }

        if seat.row_label not in seat_rows:
            seat_rows[seat.row_label] = []

        seat_rows[seat.row_label].append(seat_data)


    # Lấy ngày từ schedule (điều chỉnh theo model của bạn)
    selected_date = schedule.schedule_date if hasattr(schedule, 'schedule_date') else 'N/A'
    # Chuyển seat_rows sang danh sách có label và list ghế
    seat_rows_list = [
        {'label': row_label, 'seats': seat_rows[row_label]}
        for row_label in sorted(seat_rows.keys())
    ]

    return render(request, 'booking/ChonGhe.html', {
        'schedule': schedule,
        'movie': movie,
        'seat_rows': seat_rows_list,
        'selected_date': selected_date,
    })

def get_css_class(seat_type):
    seat_type = str(seat_type).lower()
    if seat_type == '4':
        return 'yellow'
    elif seat_type == '3':
        return 'purple'
    elif seat_type == '2':
        return 'pink'
    else:
        return 'white'
