from django.shortcuts import render, get_object_or_404
from apps.schedule.models import Schedule
from apps.seats.models import Seats
from apps.booking.models import Booking
from apps.movies.models import Movie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
import base64
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
    if seat_type == '150000':
        return 'yellow'
    elif seat_type == '120000':
        return 'purple'
    elif seat_type == '90000':
        return 'pink'
    else:
        return 'white'


def generate_qr_code(data: str) -> str:
    import qrcode
    from PIL import Image
    from io import BytesIO
    import base64

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def thanh_toan(request, movie_id, schedule_id):
    movie = get_object_or_404(Movie, id=movie_id)
    schedule = get_object_or_404(Schedule, id=schedule_id)
    total_amount = None
    if request.method == 'POST':
        seat_codes = request.POST.get("selected_seats", "").split(", ")  # ["A1", "A2", "B3"]
        seats = []
        selected_seats = []  # dùng để render lại
        
        for code in seat_codes:
            row = code[0]
            number = code[1:]
            try:
                seat = Seats.objects.get(row_label=row, number=int(number), room=schedule.room)
                seats.append(seat)
                selected_seats.append(code)
            except Seats.DoesNotExist:
                continue  # Bỏ qua nếu không tìm thấy ghế

        total_amount = request.POST.get('total_amount')
        userBooking = request.user
        
        for seat in seats:
            Booking.objects.create(
                user=userBooking,
                schedule=schedule,
                seat=seat,
                price=seat.seat_type,
                seat_status=1
            )

        #  QR code
        qr_data = f"Phim: {movie.movie_name}\nSuất chiếu: {schedule.schedule_date} {schedule.schedule_start}\nGhế: {', '.join(selected_seats)}\nTổng tiền: {total_amount} VND"
        qr_code_img = generate_qr_code(qr_data)
        print(qr_code_img)
        return render(request, 'booking/ThanhToan.html', {
            'movie': movie,
            'schedule': schedule,
            'selected_seats': selected_seats,
            'total_amount': total_amount,
            'qr_code': qr_code_img
        })

    return render(request, 'booking/ThanhToan.html', {
        'movie': movie,
        'schedule': schedule,
    })
