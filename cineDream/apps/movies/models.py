from django.db import models

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=255)
    movie_description = models.TextField()
    movie_trailer = models.TextField()
    movie_genres = models.CharField(max_length=255)
    movie_release = models.DateField()
    movie_lenght = models.TimeField()
    movie_format = models.CharField(max_length=50)
    movie_image_poster = models.TextField()

    class Meta:
        db_table = 'Movie'
        managed = False

    def __str__(self):
        return self.movie_name  # trả về tên phim