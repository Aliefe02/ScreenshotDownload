import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import uuid
import os
import shutil

# ID_Ghost = "76561198224626768"
# ID_Stewie = "76561198869949927"



def GetScreenshotLink(ID):
    return "https://steamcommunity.com/profiles/"+ID+"/screenshots/"

def GetScreenshotsLinks(ID):
    ScreenshotList = []
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    url = GetScreenshotLink(ID)
    browser.get(url)
    i = 0
    while i<10:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)   
        i += 1
    i = 0
    soup = BeautifulSoup(browser.page_source,features="lxml")
    browser.close()
    for link in soup.findAll('a'):
        if "https://steamcommunity.com/sharedfiles/filedetails" in link.get("href"):
            FullPhoto = requests.get(link.get('href'))
            soupPhoto = BeautifulSoup(FullPhoto.text,features="lxml")
            for PhotoLink in soupPhoto.findAll('a'):
                if "https://steamuserimages-a.akamaihd.net/ugc" in PhotoLink.get('href'):
                    i += 1
                    ScreenshotList.append(PhotoLink.get('href'))
                    break
    print(str(i)+" Screenshots Are Found!")
    return ScreenshotList,i

def GetZipFolder(ID):
    ScreenshotList,ScreenshotCount = GetScreenshotsLinks(ID)
    i = 1
    while True:
        folderName = str(uuid.uuid4())
        if not os.path.exists(folderName+'.zip'):
            os.mkdir(folderName)
            os.chdir(folderName)
            break

    for link in ScreenshotList:
        img = requests.get(link)
        file = open('Screenshot '+ str(i)+' .jpg','wb')
        file.write(img.content)
        i += 1
        file.close()
    os.chdir("..")
    shutil.make_archive(folderName, 'zip', folderName)
    while True:
        try:
            shutil.rmtree(folderName)
            break
        except:
            pass
    return folderName+'.zip',ScreenshotCount