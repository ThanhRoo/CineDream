from django.shortcuts import render, get_object_or_404,redirect
from apps.schedule.models import Schedule
from apps.seats.models import Seats
from apps.booking.models import Booking
from apps.movies.models import Movie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
from base64 import b64decode
import uuid
import hmac
import hashlib
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse
from apps.temporarybooking.models import TemporaryBooking
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

User = get_user_model()
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
            temp = TemporaryBooking.objects.create(
                movie=movie,
                schedule=get_object_or_404(Schedule, id=request.POST.get("schedule_id")),
                selected_seats=request.POST.get("selected_seats", ""),
                total_amount=request.POST.get("total_amount", "0")
            )

            endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
            partnerCode = "MOMO"
            accessKey = "F8BBA842ECF85"
            secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
            orderInfo = f"Thanh toán vé xem phim: {movie.movie_name}"
            redirectUrl = f"https://a11ce6e85dab.ngrok-free.app/dat-ve/momo/return?token={str(temp.token)}" # thay doi moi khi khoi dong lai ngrok
            ipnUrl = "https://a11ce6e85dab.ngrok-free.app/momo/ipn/" # thay doi moi khi khoi dong lai ngrok

            amount =  request.POST.get('total_amount')
            orderId = str(uuid.uuid4())
            requestId = str(uuid.uuid4())
            requestType = "captureWallet"
            extraData = str(temp.token)   # hoặc encode thêm info nếu cần

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
    token = request.GET.get("token")
    if not token:
        return HttpResponse("Lỗi: Không có token xác thực.")

    try:
        temp_booking = TemporaryBooking.objects.get(token=token)
    except TemporaryBooking.DoesNotExist:
        return HttpResponse("Lỗi: Không tìm thấy dữ liệu đặt vé.")

    # Trả về theo path chứa token 
    return redirect(reverse('thanh_toan', kwargs={'token': str(temp_booking.token)}))



@csrf_exempt
def momo_ipn(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    result_code = str(data.get("resultCode"))
    token = data.get("extraData")

    if result_code == "0" and token:
        try:
            temp_booking = TemporaryBooking.objects.get(token=token)
        except TemporaryBooking.DoesNotExist:
            return JsonResponse({"message": "Không tìm thấy đặt chỗ"}, status=400)

        # Bạn có thể xử lý lưu vé chính thức ở đây nếu muốn

        return JsonResponse({"message": "IPN received successfully"}, status=200)

    return JsonResponse({"message": "Thanh toán thất bại"}, status=400)


def thanh_toan(request, token):
    temp = get_object_or_404(TemporaryBooking, token=token)
    movie = Movie.objects.get(id=temp.movie.id)
    schedule = temp.schedule
    booking_seats = temp.selected_seats
    
    seat_codes = booking_seats.split(", ")
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

    total_amount = temp.total_amount
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

    user = User.objects.get(username = userBooking)
    send_ticket_email(user.email,user.username,schedule.schedule_date,schedule.schedule_start,booking_seats,qr_code_img)
    
    return render(request, 'booking/Ve.html', {
        'movie': movie,
        'schedule': schedule,
        'selected_seats': selected_seats,
        'total_amount': total_amount,
        'qr_code': qr_code_img
    })



def send_ticket_email(user_email, user_name, schedule_date , schedule_start , seats, qr_code_img):

    email = EmailMessage(
        subject="Xác nhận đặt vé - CineDream 🎬",
        body=f"Xin chào {user_name},\n\nBạn đã đặt vé thành công!\n\nThông tin vé:\nSuất chiếu:{schedule_date} {schedule_start}\nGhế:{seats}\n\nQR code được đính kèm để quét tại rạp.",
        from_email="CineDream <your_email@gmail.com>",
        to=[user_email],
    )
    qr_base64 = qr_code_img.split(',')[1]  # loại bỏ phần 'data:image/png;base64,'
    # Chuyển về dạng bytes
    qr_image_bytes = b64decode(qr_base64)

    email.attach("ticket_qr.png", qr_image_bytes, "image/png")
    email.send()
