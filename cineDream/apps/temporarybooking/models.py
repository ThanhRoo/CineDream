from django.db import models
import uuid
from apps .movies.models import Movie
from apps.schedule.models import Schedule
# Create your models here.

class TemporaryBooking(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    selected_seats = models.CharField(max_length=255)
    total_amount = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100, null=True)