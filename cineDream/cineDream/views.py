from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

def home_page(request):
    return render(request, 'TrangChu.html')

def login(request):
    return render(request,'login.html')
