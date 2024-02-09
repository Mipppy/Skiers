# Scans all links in underdogtiming and gets a all the race data for every nordic race
import io
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from io import StringIO, BytesIO
headers = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}

def scanPDFs(list):
    biglist = []
    for url in list:
        response = requests.get(url=url, headers=headers, timeout=120)
        on_fly_mem_obj = io.BytesIO(response.content)
        pdf_file = PdfReader(on_fly_mem_obj)
        biglist.append(parsePDF(pdf_file.pages, url))
    return biglist

def parsePDF(pages,url):
    page_text = []
    for page in pages:
        page_text.append(page.extract_text())
    return page_text

def mainPDFFunc():
    url = 'https://www.underdogtiming.com/general-5'
    response = requests.get(url=url, headers=headers, timeout=120)
    soup = BeautifulSoup(response.content, 'html.parser')
    segments = soup.find_all('p', class_="font_8")
    goodsegs = []
    for seg in segments:
        seg = str(seg)
        if seg.find("Nordic") != -1:
            minsoup = BeautifulSoup(seg, 'html.parser')
            minseg = minsoup.find_all('a')
            for seg2 in minseg:
                if "underdogtiming.com/_files" in str(seg2['href']):
                    goodsegs.append(seg2['href'])
    return goodsegs

def PDFreadline(text):
    return text.split('\\n')

def PDFListedData(hrefs):
    allPDFdata = []
    for data in scanPDFs(hrefs):
        if all(element == "" for element in data) == False:
            allPDFdata.append(PDFreadline(str(data)))