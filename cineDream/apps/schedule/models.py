from django.db import models

# Create your models here.

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey('movies.Movie', on_delete=models.DO_NOTHING, db_column='movie_id')
    room = models.ForeignKey('room.Room', on_delete=models.DO_NOTHING, db_column='room_id')
    schedule_date = models.DateField()
    schedule_start = models.TimeField()
    schedule_end = models.TimeField()

    class Meta:
        db_table = 'Schedule'
        managed = False
    def __str__(self):
        return f"{self.movie.movie_name} - {self.schedule_date} {self.schedule_start.strftime('%H:%M')}"