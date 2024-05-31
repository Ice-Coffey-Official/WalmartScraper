import requests
from bs4 import BeautifulSoup
from util.config import retryBackoff, reqSleep, baseURL
import time
import random

def getRandTime(t=1.5, v=0.5):
    num = t - v + t*random.random()
    return num

def extractLinks(url):
    time.sleep(getRandTime())
    newLinks = []
    header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
    }
    try:
        page = requests.get(url, headers=header)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=header)
        except:
            return []

    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "mt3 dark-gray no-underline db f6"})
    
    for i in range(len(mylinks)):
        link = mylinks[i]
        newLink = baseURL + link['href']
        newLinks.append(newLink)
    
    return newLinks

def extractCityLinks(url):
    time.sleep(getRandTime())
    newLinksStore = []
    newLinksCity = []
    header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
    }
    try:
        page = requests.get(url, headers=header)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=header)
        except:
            return []

    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "dark-gray no-underline dbi f6"})
    
    for i in range(len(mylinks)):
        if not i:
            continue
        link = mylinks[i]
        newLink = link['href']
        if 'store-directory' in newLink:
            newLinksCity.append(baseURL + newLink)
        else:
            newLinksStore.append(baseURL + newLink)

    return newLinksCity, newLinksStore

def extractStoreLinks(url):
    time.sleep(getRandTime())
    newLinks = []
    header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
    }
    try:
        page = requests.get(url, headers=header)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=header)
        except:
            return []

    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "black no-underline dbi f6 b"})

    for i in range(len(mylinks)):
        link = mylinks[i]
        newLink = baseURL + link['href']
        newLinks.append(newLink)
    
    return newLinks


def extractStoreInfo(url):
    time.sleep(getRandTime())
    newLinks = []
    header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
    }
    try:
        page = requests.get(url, headers=header)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=header)
        except:
            return []

    soup = BeautifulSoup(page.text, 'lxml')
    try:
        storeNum = url.split('/')[-1].split('-')[0]
        city = url.split('/')[-1].split('-')[1]
        state = url.split('/')[-1].split('-')[2]
    except:
        print(url)
        storeNum = ''
        city = ''
        state = ''
    try:
        name = soup.find("h1", { "class" : "ma0 bold lh-title f3 f1-m" }).text
    except:
        name = ''

    try:
        phoneNumber = soup.find("a", { "class" : "mr3 dark-gray f6" }).text
    except:
        phoneNumber = ''

    try:
        address = soup.find("span", { "class" : "ma0 normal f5 dark-gray" }).text.replace('\n', '')
    except:
        address = ''

    try:
        coords = soup.findAll("script", { "id" : "__NEXT_DATA__" })[-1].text
        latitude = coords.split('latitude":')[-1][:9]
        longitude = coords.split('longitude":')[-1][:9]
    except:
        latitude = ''
        longitude = ''

    return [name, storeNum, phoneNumber, address, url, longitude, latitude, city, state]
