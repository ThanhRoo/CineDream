from django.shortcuts import render, get_object_or_404,redirect
from apps.schedule.models import Schedule
from apps.seats.models import Seats
from apps.booking.models import Booking
from apps.movies.models import Movie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
import base64
import uuid
import hmac
import hashlib
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse

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


def thanh_toan_momo(request, movie_id): 
        movie = get_object_or_404(Movie, id=movie_id)

        if request.method == 'POST':
        # Gọi API MoMo
            request.session['booking_data'] = {
            'movie_id': movie.id,
            'schedule_id': request.POST.get("schedule_id", None),
            'selected_seats': request.POST.get("selected_seats", ""),  # "A1, A2"
            'total_amount': request.POST.get("total_amount", "0")
            }
            endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
            partnerCode = "MOMO"
            accessKey = "F8BBA842ECF85"
            secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
            orderInfo = f"Thanh toán vé xem phim: {movie.movie_name}"
            redirectUrl = "https://11001214f920.ngrok-free.app/dat-ve/momo/return/" # ← thay bằng domain thật
            ipnUrl = "https://11001214f920.ngrok-free.app/momo/ipn/"          # ← thay bằng domain thật
            amount =  request.POST.get('total_amount')
            orderId = str(uuid.uuid4())
            requestId = str(uuid.uuid4())
            requestType = "captureWallet"
            extraData = ""  # hoặc encode thêm info nếu cần

            rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
            signature = hmac.new(
                                bytes(secretKey, 'utf-8'),
                                bytes(rawSignature, 'utf-8'),
                                hashlib.sha256
                            ).hexdigest()

            data = {
                "partnerCode": partnerCode,
                "partnerName": "Cinema",
                "storeId": "CinemaBookingSystem",
                "requestId": requestId,
                "amount": amount,
                "orderId": orderId,
                "orderInfo": orderInfo,
                "redirectUrl": redirectUrl,
                "ipnUrl": ipnUrl,
                "lang": "vi",
                "extraData": extraData,
                "requestType": requestType,
                "signature": signature
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(endpoint, data=json.dumps(data), headers=headers)
            result = response.json()

            if result.get("payUrl"):
                return redirect(result["payUrl"])  # Chuyển user sang MoMo thanh toán
            else:
                return HttpResponse("Không thể tạo link thanh toán MoMo", status=500)

def momo_return(request):
    print("Session Keys:", request.session.keys())
    print("Full session data:", dict(request.session))

    result_code = request.GET.get("resultCode")
    message = request.GET.get("message")

    if result_code == "0":
        booking_data = request.session.get('booking_data')
        if not booking_data:
            return HttpResponse("Lỗi: Không tìm thấy dữ liệu đặt vé.")

        movie_id = booking_data['movie_id']
        schedule_id = booking_data['schedule_id']

        return redirect(
            reverse('thanh_toan', args=[movie_id, schedule_id])
        )
    return HttpResponse("❌ Thanh toán thất bại: " + message)


@csrf_exempt
def momo_ipn(request):
    result_code = request.GET.get("resultCode")
    message = request.GET.get("message")

    if result_code == "0":
        booking_data = request.session.get('booking_data')
        if not booking_data:
            return HttpResponse("Lỗi: Không tìm thấy dữ liệu đặt vé.")

        movie_id = booking_data['movie_id']
        schedule_id = booking_data['schedule_id']

        # Redirect tới thanh_toan để lưu vé và tạo QR
        return redirect(
            reverse('thanh_toan', args=[movie_id, schedule_id])
        )

    return HttpResponse("❌ Thanh toán thất bại: " + message)

def thanh_toan(request, movie_id, schedule_id):
    movie = get_object_or_404(Movie, id=movie_id)
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    booking_data = request.session.get('booking_data')
    if booking_data:
        seat_codes = booking_data.get("selected_seats", "").split(", ")
        seats = []
        selected_seats = []

        for code in seat_codes:
            row = code[0]
            number = code[1:]
            try:
                seat = Seats.objects.get(row_label=row, number=int(number), room=schedule.room)
                seats.append(seat)
                selected_seats.append(code)
            except Seats.DoesNotExist:
                continue

        total_amount = booking_data.get("total_amount")
        userBooking = request.user

        for seat in seats:
            Booking.objects.create(
                user=userBooking,
                schedule=schedule,
                seat=seat,
                price=seat.seat_type,
                seat_status=1
            )

        qr_data = f"Phim: {movie.movie_name}\nSuất chiếu: {schedule.schedule_date} {schedule.schedule_start}\nGhế: {', '.join(selected_seats)}\nTổng tiền: {total_amount} VND"
        qr_code_img = generate_qr_code(qr_data)

        return render(request, 'booking/ThanhToan.html', {
            'movie': movie,
            'schedule': schedule,
            'selected_seats': selected_seats,
            'total_amount': total_amount,
            'qr_code': qr_code_img
        })

    # Không có session, render lại trang trung gian
    return render(request, 'booking/Ve.html', {
        'movie': movie,
        'schedule': schedule,
    })
