from django.shortcuts import render, HttpResponse
from .helpers.pdf import * 


def index(request):
    hrefs = mainPDFFunc()
    allPDFdata = PDFListedData(hrefs)
    parseRacerData(allPDFdata)
    return render(request, "skiers/index.html", {"links":hrefs, "pdf":allPDFdata})


def rescan(request):
    hrefs = mainPDFFunc()
    allPDFdata = PDFListedData(hrefs)