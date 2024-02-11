from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .helpers.pdf import * 
from .models import *
from django.urls import reverse


def index(request):
    results = Result.objects.all()
    print(results)
    return render(request, "skiers/index.html", {"results": results})

def rescan(request):
    hrefs = mainPDFFunc()
    allPDFdata = PDFListedData(hrefs)
    parseRacerData(allPDFdata)
    return HttpResponseRedirect(reverse("index"))