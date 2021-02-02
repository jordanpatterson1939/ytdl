# -*- coding: utf-8 -*-
import os
import json
import pyperclip as pc
import subprocess
import pytube
from http.client import RemoteDisconnected
from socket import gaierror
from urllib.error import URLError


f = open('config.json','r')
folders = json.load(f)
musicfolder = folders['musicfolder']
videofolder = folders['videofolder']

def getvideofromurl(url):
    print("####  Getting Video from url: {0}".format(url))
    video = pytube.YouTube(url,on_progress_callback=progressBar)
    #print("#### {0}".format(video.title))
    return video

def viewstreamsfordownload(streams,title,mp3=True):
    bitrates = {}
    for s in streams.filter(only_audio=True):
        bitrates[int(s.abr.strip('kbps'))] = s
    # print("####  Bitrates: ",list(bitrates.keys()))
    fastest = max(list(bitrates.keys()))
    if mp3:
        return bitrates[fastest]
    resolutions = ['1080p','720p','480p','360p','240p','144p']
    for r in resolutions:
        objs = streams.filter(only_video=True,res=r)
        if objs==None:
            continue
        else:
            return bitrates[fastest],objs[0]

banner = '''
 ▄· ▄▌      ▄• ▄▌▄▄▄▄▄▄• ▄▌▄▄▄▄· ▄▄▄ .    ·▄▄▄▄        ▄▄▌ ▐ ▄▌ ▐ ▄ ▄▄▌         ▄▄▄· ·▄▄▄▄  ▄▄▄ .▄▄▄  
▐█▪██▌▪     █▪██▌•██  █▪██▌▐█ ▀█▪▀▄.▀·    ██▪ ██ ▪     ██· █▌▐█•█▌▐███•  ▪     ▐█ ▀█ ██▪ ██ ▀▄.▀·▀▄ █·
▐█▌▐█▪ ▄█▀▄ █▌▐█▌ ▐█.▪█▌▐█▌▐█▀▀█▄▐▀▀▪▄    ▐█· ▐█▌ ▄█▀▄ ██▪▐█▐▐▌▐█▐▐▌██▪   ▄█▀▄ ▄█▀▀█ ▐█· ▐█▌▐▀▀▪▄▐▀▀▄ 
 ▐█▀·.▐█▌.▐▌▐█▄█▌ ▐█▌·▐█▄█▌██▄▪▐█▐█▄▄▌    ██. ██ ▐█▌.▐▌▐█▌██▐█▌██▐█▌▐█▌▐▌▐█▌.▐▌▐█ ▪▐▌██. ██ ▐█▄▄▌▐█•█▌
  ▀ •  ▀█▄▀▪ ▀▀▀  ▀▀▀  ▀▀▀ ·▀▀▀▀  ▀▀▀     ▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀ ▀▪▀▀ █▪.▀▀▀  ▀█▄▀▪ ▀  ▀ ▀▀▀▀▀•  ▀▀▀ .▀  ▀


'''
downloadindicator='''
\t░░░░░░░░░░░║
\t░░▄█▀▄░░░░░║░░░░░░▄▀▄▄
\t░░░░░░▀▄░░░║░░░░▄▀
\t░▄▄▄░░░░█▄▄▄▄▄▄█░░░░▄▄▄
\t▀░░░▀█░█▀░░▐▌░░▀█░█▀░░░▀
\t░░░░░░██░░▀▐▌▀░░██
\t░▄█▀▀▀████████████▀▀▀█
\t█░░░░░░██████████░░░░░▀▄
\t█▄░░░█▀░░▀▀▀▀▀▀░░▀█░░░▄█
\t░▀█░░░█░░░░░░░░░░█░░░█▀
'''
def savemp3(stream,title):
    try:
        os.chdir(musicfolder)
    except FileNotFoundError:
        print("\nIt appears that your config variables were not \nset, or the folder you entered to save audio/mp3 files \ndoes not exist. Not sure where to save. Aborting.")
        exit(1)
    print(downloadindicator)
    print("\t"+title.replace('"',''))
    try:
        stream.download(filename='temp')
    except (ConnectionResetError,gaierror,RemoteDisconnected,URLError):
        print('''
\t──▒▒▒▒▒▒───▄████▄
\t─▒─▄▒─▄▒──███▄█▀
\t─▒▒▒▒▒▒▒─▐████──█─█
\t─▒▒▒▒▒▒▒──█████▄
\t─▒─▒─▒─▒───▀████▀
''')
        print("There was a network error while attempting to download the file, \nkindly verify that you have an internet connection and try gain in a moment.\nGoodbye, for now.")
        exit(1)
    destination = title+'.mp3'
    destination = destination.replace('"','')
    FNULL = open(os.devnull, 'w')
    ffmpeg = 'ffmpeg -i {0} -vn -ab 128k -ar 44100 -y "{1}"'.format('temp.webm',destination)
    subprocess.run(ffmpeg,stdout=FNULL,stderr=subprocess.STDOUT)
    os.remove('temp.webm')


def savevideo(audiostream,videostream,title):
    try:
        os.chdir(videofolder)
    except FileNotFoundError:
        print("\nIt appears that your config variables were not \nset, or the folder you entered to save video files \ndoes not exist. Not sure where to save. Aborting.")
        exit(1)
    print(downloadindicator)
    print("\t"+title.replace('"',''))
    try:
        audiostream.download(filename='temp')
        videostream.download(filename='temp')
    except (ConnectionResetError,gaierror,RemoteDisconnected,URLError):
        print('''
\t──▒▒▒▒▒▒───▄████▄
\t─▒─▄▒─▄▒──███▄█▀
\t─▒▒▒▒▒▒▒─▐████──█─█
\t─▒▒▒▒▒▒▒──█████▄
\t─▒─▒─▒─▒───▀████▀
''')
        print("There was a network error while attempting to download the files, \nkindly verify that you have an internet connection and try gain in a moment.\nGoodbye, for now.")
        exit(1)
    destination = title.replace('"','').replace(':','-')+'.mp4'
    command = 'ffmpeg -i {0} -i {1} -acodec copy -c:v copy "{2}"'.format('temp.webm','temp.mp4',destination)
    FNULL = open(os.devnull, 'w')
    #progress bar
    subprocess.run(command,stdout=FNULL,stderr=subprocess.STDOUT)
    os.remove('temp.webm')
    os.remove('temp.mp4')

def progressBar(stream,chunk,bytes_remaining):
    totalSize = stream.filesize
    downloaded = totalSize - bytes_remaining
    percent = "{0:.1f}".format(100*downloaded/float(totalSize))
    fillLength = int(50*downloaded//totalSize)
    bar = '█'*fillLength+'-'*(50-fillLength)
    print(f'Downloading: |{bar}| {percent}% Complete',end='\r')
    if totalSize==downloaded:
        print()

def getdownloadoption(title):
    while True:
        print("####  Select your download option for: {0}".format(title))
        print("####  (a) AUDIO    (v) VIDEO    (q) EXIT")
        print("####  Enter: ",end='')
        while True:
            opt = input().upper()
            if opt=='A' or opt=='V':
                break
            elif opt=='Q':
                exit(1)
            print("####  Enter 'a' for Audio OR 'v' for Video OR 'q' to Exit: ",end='')
        return opt

def menu():
    while True:
        #print("\n\n@#$&  ::WELCOME YO YOUR YOUTUBE DOWNLOADER::\n")
        print("####  (a) PASTE LINK\t(q) EXIT")
        print("####  Enter: ",end='')
        while True:
            choice = input().upper()
            if choice=='A' or choice=='Q':
                break
            print("####  Enter 'a' to paste a link or 'q' to close the program: ",end='')
        if choice=='A':
            url = pc.paste()
            while True:
                try:
                    video = getvideofromurl(url)
                    break
                except pytube.exceptions.RegexMatchError:
                    print("####  The link provided was not valid.\n####  Please paste a valid link here or type'q' to quit: ",end='')
                    url = input()
                    if url.upper()=='Q':
                        exit(1)
                except (RemoteDisconnected,gaierror,URLError,ConnectionResetError):
                    print("####  There was a network error while attempting to fetch video data. Try again later.")
                    exit(1)
        
            opt = getdownloadoption(video.title)
            if opt=='A':
                stream = viewstreamsfordownload(video.streams,video.title,mp3=(opt=='A'))              
                savemp3(stream,video.title)
            else:
                audio_stream,video_stream = viewstreamsfordownload(video.streams,video.title,mp3=(opt=='A'))
                savevideo(audio_stream,video_stream,video.title)
        elif choice=='Q':
            print("\n\t\tExitting. Good-bye!")
            break

def main():
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')
    print(banner)
    menu()

if __name__=='__main__':
    main()
