from django.shortcuts import render
from django.http import FileResponse
from .ScreenshotDownloader import *
import os
import threading
import time

def deleteZip(Filename):
    time.sleep(5)
    os.remove(Filename)

def index(request):
    return render(request, 'index.html')

def CreateZip(request):
    Filename,ScreenshotCount = GetZipFolder(request.POST['ID'])
    return render(request,'index.html',{'ScreenshotCount':ScreenshotCount,'Filename':Filename})

def download(request, Filename=''):
    zip_file = open(Filename, 'rb')
    RemoveThread = threading.Thread(target=deleteZip,args=[Filename])
    RemoveThread.start()
    return FileResponse(zip_file)
