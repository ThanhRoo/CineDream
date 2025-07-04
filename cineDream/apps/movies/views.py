from django.shortcuts import render
from .models import Movie
# Create your views here.
from urllib.parse import urlparse, parse_qs

def trang_chu(request):
    return render(request, 'home')

def extract_youtube_id(url):
    try:
        query = urlparse(url)
        return parse_qs(query.query)['v'][0]
    except:
        return ''

def chiTietPhim(request, phim_id):
    phim = Movie.objects.get(id=phim_id)
    trailer_id = extract_youtube_id(phim.movie_trailer)
    return render(request, 'movies/ChiTietPhim.html', {'phim': phim, 'trailer_id': trailer_id})



def danhSachPhim(request):
    ds_phim = Movie.objects.all()
    return render(request, 'movies/Phim.html',{'ds_phim': ds_phim})