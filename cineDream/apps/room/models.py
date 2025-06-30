from django.db import models

# Create your models here.
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100)
    cinema = models.ForeignKey('cinema.Cinema', on_delete=models.DO_NOTHING, db_column='cinema_id')
    

    class Meta:
        db_table = 'Room'
        managed = False
    def __str__(self):
        return self.room_name