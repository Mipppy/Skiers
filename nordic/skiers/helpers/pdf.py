# Scans all links in underdogtiming and gets a all the race data for every nordic race
import io,re
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from io import StringIO, BytesIO
from ..models import *
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
        if seg.find("Nordic") != -1 or seg.find("JNQ") != -1:
            minsoup = BeautifulSoup(seg, 'html.parser')
            minseg = minsoup.find_all('a')
            for seg2 in minseg:
                if "underdogtiming.com/_files" in str(seg2['href']) and str(seg2).find("Team") == -1 and str(seg2).find("Start") == -1:
                    goodsegs.append(seg2['href'])
    for segment in goodsegs:
        site = Sites(site=segment)
        site.save()
    return goodsegs

def PDFreadline(text):
    return text.split('\\n')

def PDFListedData(hrefs):
    allPDFdata = []
    for data in scanPDFs(hrefs):
        if all(element == "" for element in data) == False:
            allPDFdata.append(PDFreadline(str(data)))
    return allPDFdata

def parseRacerData(data):
    for sub in data:
        for race in sub:
            if race != "":
                try:
                    race = str(race).split(" ")
                    race = [item for item in race if item != ""]
                    time_pattern = re.compile(r'^:(\d{2}:\d{2}.\d)$')
                    score_pattern = re.compile(r'\d+(\.\d+)?')
                    if race[0].isdigit() and race[1].isdigit() and time_pattern.match(race[2]) and score_pattern.match(race[3]) and race[4].isalpha():
                        addRaceToDatabase(race)
                except Exception as e:
                    continue
def addRaceToDatabase(race):
    racer = racerExistsAlready(race)
    print(f"racer {racer} |time {race[2]} | bib={race[0]} | place={race[1]} | score={race[3]}")
    racer_result = Result(racer=racer[0], time=race[2], bib=int(race[0]), place=int(race[1]), score=float(race[3]))
    racer_result.save()
    
    
def racerExistsAlready(race):
    firstname = None
    lastname = None
    elements_before_float = []
    for index, element in enumerate(race):
        if element and element[0].isupper() and all(c.islower() or not c.isalpha() for c in element[1:]) and not any(c.isdigit() for c in element):
            firstname = element
            lastname = race[index-1]
            i = index-1
            while i > 3:
                i -= 1
                elements_before_float.insert(0,race[i])
    racerQuery = Racer.objects.filter(firstname=firstname, lastname=lastname)
    if not racerQuery:
        new_racer = Racer(firstname=firstname, lastname=lastname, team=" ".join(elements_before_float))
        new_racer.save()
        return new_racer
    else:
        return racerQuery
# Racer.objects.all().delete()
# Result.objects.all().delete()