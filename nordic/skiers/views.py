from django.shortcuts import render, HttpResponse
from .helpers.pdf import pdfWork

def index(request):
    return render(request, "skiers/index.html")