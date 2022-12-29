from pytube import YouTube
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading
import tkinter as tk
import pytube
import sys



def on_progress(vid, chunk, bytes_remaining):
    
    total_size = vid.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    totalsz = (total_size/1024)/1024
    totalsz = round(totalsz, 1)
    remain = (bytes_remaining / 1024) / 1024
    remain = round(remain, 1)
    dwnd = (bytes_downloaded / 1024) / 1024
    dwnd = round(dwnd, 1)
    percentage_of_completion = round(percentage_of_completion, 2)
    
    
   
    print('Download Progess: {per}%\r'.format(
        per=percentage_of_completion), end='')


def progress_function(vid, chunk, bytes_remaining):
    filesize = vid.filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write('|{bar}| {percent}%\r'.format(
        bar=status, percent=percent))
    sys.stdout.flush()


def playlist_downloader(link, folder):
    yt = pytube.Playlist(link)
    i = 1
    for y in yt.video_urls:
        video = pytube.YouTube(y)
        print("\n"+str(i)+'. Downloading: '+video.title)
        video.register_on_progress_callback(on_progress)
        v = video.streams.get_highest_resolution()
        print('\nFile Size: '+str(round(v.filesize/(1024*1024), 1))+' MB\n')
        v.download(filename="Video_"+str(i).zfill(2) +
                   ".mp4", output_path=folder)
        i = i+1


def youtube_downloader(link, folder):
    video = pytube.YouTube(link)
    print('Downloading: '+video.title)
    video.register_on_progress_callback(on_progress)
    v = video.streams.get_highest_resolution()
    print('\nFile Size: '+str(round(v.filesize/(1024*1024), 1))+' MB\n')
    v.download(output_path=folder)


def Browse():
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")
    path.set(download_Directory)


def Download():
    link = link_text.get()
    video = pytube.YouTube(link)
    video_name.set(video.title)
    v = video.streams.get_highest_resolution()
    video.register_on_progress_callback(on_progress)
    folder = path_text.get()
    v.download(output_path=folder)

def TH():
    threading.Thread(target=Download).start()

def stop():
    quit()


link = "https://www.youtube.com/watch?v=GMR3RUAz_pE"
video = pytube.YouTube(link)
print('Downloading: '+video.title)
video.register_on_progress_callback(on_progress)

info = []
a = video.streams.filter(only_audio=True).order_by('filesize')
a = a.__reversed__()
for b in a:
   
    print(b.type, b.mime_type, b.abr, round(b.filesize/(1024*1024), 1))
    i = []
    i.append(b.type)
    i.append(b.mime_type.split('/')[1])
    i.append(b.abr)
    i.append(round(b.filesize/(1024*1024), 1))
    i.append(b.itag)
    info.append(i)


a = video.streams.filter(only_video=True).order_by('filesize')
a = a.__reversed__()
for b in a:   
    print(b.type, b.mime_type, b.resolution , round(b.filesize/(1024*1024), 1))
    i = []
    i.append(b.type)
    i.append(b.mime_type.split('/')[1])
    i.append(b.resolution)
    i.append(round(b.filesize/(1024*1024), 1))
    i.append(b.itag)
    info.append(i)

lst = video.streams.all()

for l in lst:
    print(l)