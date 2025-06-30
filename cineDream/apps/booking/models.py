from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # <- Gán User từ hệ thống auth

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')

    seat = models.ForeignKey('seats.Seats', on_delete=models.DO_NOTHING, db_column='seat_id')
    schedule = models.ForeignKey('schedule.Schedule', on_delete=models.DO_NOTHING, db_column='schedule_id')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seat_status = models.CharField(max_length=20)

    class Meta:
        db_table = 'Booking'
    def __str__(self):
        return f"Booking {self.id} - User: {self.user.username} - Seat: {self.seat} - Schedule: {self.schedule}"
