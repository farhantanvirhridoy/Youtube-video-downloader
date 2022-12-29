from pytube import YouTube
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading
import tkinter as tk
import pytube
import sys
import os





root = Tk()
root.title("Youtube Video Downloader")

path = StringVar()
link = StringVar()
video_name = StringVar()
percentage = StringVar()
downloaded = StringVar()


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
    downloaded.set(str(dwnd)+"/"+str(totalsz)+"\nMB")
    percentage.set("Downloading\n"+str(percentage_of_completion)+"%")
    if percentage_of_completion == 100: 
        percentage.set("Download\nCompleted")
        messagebox.showinfo(title="Download Completed",message="Download completed and save video in "+path_text.get())

    progress_bar['value'] = percentage_of_completion
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
    global info
    link = link_text.get()
    video = pytube.YouTube(link)
    video_name.set(video.title)
    index = listbox.index(ACTIVE)
    itag = info[index][4]
    v = video.streams.get_by_itag(itag)
    video.register_on_progress_callback(on_progress)
    folder = path_text.get()
    if info[index][0] == 'video':
        v.download(output_path=folder)
    else:
        filename = v.default_filename.split('.')[0] + '.mp3'
        v.download(filename=filename, output_path=folder)

def Check():
    global info 
    link = link_text.get()
    video = pytube.YouTube(link)
    print('Downloading: '+video.title)
    video.register_on_progress_callback(on_progress)

    info = []
    


    a = video.streams.filter(type='video', progressive=True).order_by('filesize')
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

    a = video.streams.filter(type='audio').order_by('filesize')
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

    for lst in info:
        value = lst[0] + '  ' + lst[1] + '  ' + lst[2] + '  ' + str(lst[3]) + 'MB'
        value = f"{lst[0]} {lst[1]} {lst[2]} {lst[3]} MB"
        listbox.insert(END, value)

    download_button.grid(row=0,column=1)
    check_button.grid_remove()

def TH():
    threading.Thread(target=Download).start()

def check_TH():
    threading.Thread(target=Check).start()


def stop():
    
    root.quit()
    
    

head_label = Label(root, text="Youtube Video Downloader", font="Cambria 20")
head_label.grid(row=0, column=0, columnspan=3, pady=10)

link_label = Label(root, text="Youtube Link:", bg="salmon")
link_label.grid(row=1, column=0, pady=5)

link_text = Entry(root, width=90, textvariable=link)
link_text.grid(row=1, column=1)

path_label = Label(root, text="Destination:", bg="salmon", padx=6)
path_label.grid(row=2, column=0)

path_text = Entry(root,width=90, textvariable=path)
path_text.grid(row=2, column=1)

browse_button = Button(root, text="Browse", padx=5, command=Browse)
browse_button.grid(row=2, column=2)

listbox = Listbox(root, width=80)
listbox.grid(row=3, columnspan=3)

f = Frame(root)
f.grid(row=4, columnspan=3)


check_button = Button(f, text="Check", padx=10, pady=10,
                         font="Cambria 14", command=check_TH)
check_button.grid(row=0, column=0, padx=5)

download_button = Button(f, text="Download", padx=10, pady=10,
                         font="Cambria 14", command=TH)
download_button.grid(row=0, column=1, padx=5)
download_button.grid_remove()

name_label = Label(root, textvariable=video_name)
name_label.grid(row=5, columnspan=3)

progress_frame = Frame(root)
progress_frame.grid(row=6, columnspan=3)

progress_label = Label(progress_frame, textvariable=percentage)
progress_label.grid(row=0, column=0)

progress_bar = ttk.Progressbar(
    progress_frame, mode="determinate", orient="horizontal", length=480)
progress_bar.grid(row=0, column=1)

downloaded_label = Label(progress_frame, textvariable=downloaded)
downloaded_label.grid(row=0, column=2)

stop_button = Button(root, text="Stop\ndownload",command=stop)
stop_button.grid(row=7, columnspan=3, pady=10)


root.mainloop()
