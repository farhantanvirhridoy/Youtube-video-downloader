from pytube import YouTube
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading
import tkinter as tk
import pytube
import sys

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

head_label = Label(root, text="Youtube Video Downloader", font="Cambria 20")
head_label.grid(row=0, column=0, columnspan=3, pady=10)

link_label = Label(root, text="Youtube Link:", bg="salmon")
link_label.grid(row=1, column=0, pady=5)

link_text = Entry(root, width=100, textvariable=link)
link_text.grid(row=1, column=1, columnspan=2)

path_label = Label(root, text="Destination:", bg="salmon", padx=6)
path_label.grid(row=2, column=0)

path_text = Entry(root, width=87, textvariable=path)
path_text.grid(row=2, column=1)

browse_button = Button(root, text="Browse", padx=5, command=Browse)
browse_button.grid(row=2, column=2)

download_button = Button(root, text="Download", padx=10, pady=10,
                         font="Cambria 14", command=TH)
download_button.grid(row=3, columnspan=3, pady=20)

name_label = Label(root, textvariable=video_name)
name_label.grid(row=4, columnspan=3)

progress_label = Label(root, textvariable=percentage)
progress_label.grid(row=5, column=0, pady=10)

progress_bar = ttk.Progressbar(
    root, mode="determinate", orient="horizontal", length=350)
progress_bar.grid(row=5, column=1)

downloaded_label = Label(root, textvariable=downloaded)
downloaded_label.grid(row=5, column=2)

stop_button = Button(root, text="Stop\ndownload",command=stop)
stop_button.grid(row=6, columnspan=3, pady=10)


root.mainloop()
