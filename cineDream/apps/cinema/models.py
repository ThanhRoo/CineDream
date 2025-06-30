from django.db import models

# Create your models here.

class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    cinema_name = models.CharField(max_length=200)
    cinema_address = models.CharField(max_length=255)

    class Meta:
        db_table = 'Cinema'
        managed = False
    def __str__(self):
        return self.cinema_name  # trả về tên rạp chiếu phim