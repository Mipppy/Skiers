from django.shortcuts import render, HttpResponse
from .helpers.pdf import * 
import random

def index(request):
    hrefs = mainPDFFunc()
    allPDFdata = PDFListedData(hrefs)
    if random.randint(1,15) == 10:
        
    return render(request, "skiers/index.html", {"links":hrefs, "pdf":allPDFdata})