from django.db import models

# Create your models here.
class Seats(models.Model):
    id = models.AutoField(primary_key=True)
    seat_type = models.IntegerField()
    room = models.ForeignKey('room.Room', on_delete=models.DO_NOTHING, db_column='room_id')
    row_label = models.CharField(max_length=5)
    number = models.IntegerField()

    class Meta:
        db_table = 'Seats'
        managed = False
    def __str__(self):
        return f"{self.row_label}{self.number} - {self.seat_type}"