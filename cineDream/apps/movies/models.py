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


    def get_lenght_minutes(self):
        """Trả về độ dài phim tính bằng phút."""
        return self.movie_lenght.hour * 60 + self.movie_lenght.minute
    
    class Meta:
        db_table = 'Movie'
        managed = False

    def __str__(self):
        return self.movie_name  # trả về tên phim