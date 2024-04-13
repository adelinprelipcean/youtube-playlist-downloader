import pytube
from pytube import Playlist
from moviepy.editor import *
import os
from tkinter import *
import customtkinter
import tkinter as tk
import threading

### Installing required packages and creating songs output folder ###

os.system("pip install -r requirements.txt")

if not os.path.exists("./Songs"):
    os.makedirs("./Songs")

### TKINTER GUI INTERFACE BELOW ###  

root = customtkinter.CTk()
root.geometry("600x600")
root.title("Play.listed Downloader")
root.resizable(False, False)

bg = PhotoImage(file = "background.png")

label1 = Label(root, image = bg)
label1.place(x=-2,y=-2)

def download():
    playlist_link = text_box.get(1.0, "end-1c")
    threading.Thread(target=download_playlist, args=(playlist_link,)).start()   

    """ Downloading all the songs in .mp4 format """
def download_playlist(playlist_link):
    playlist = Playlist(playlist_link)
    output_text.insert(tk.END, 'Number of videos in playlist: %s\n' % len(playlist.video_urls))
    
    for link in playlist:
        yt = pytube.YouTube(link)
        stream = yt.streams.filter(mime_type="video/mp4", progressive=False).first()
        name = yt.title
        stream.download("./Songs")
        output_text.insert(tk.END, name[:20]+"..."+" downloaded in MP4.\n")
        
    """ Converting all the files from video.mp4 to audio.mp3 format """

    for file in os.listdir("./Songs"):
        if file.endswith(".mp4"):
            video_clip = VideoFileClip("./Songs/"+file)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile("./Songs/"+file[:-4]+'.mp3')
            audio_clip.close()
            video_clip.close()
  
        else:
            continue

    """ After succesfully converting all the .mp4 files,
    we need to delete them so there will remain .mp3 files only """

    for file in os.listdir("./Songs"):
        if file.endswith(".mp4"):
            os.remove("./Songs/"+file)

    output_text.insert(tk.END, "ALL OPERATIONS ARE DONE! YOU CAN LISTEN TO YOUR FAVORITE SONGS NOW!")


button = customtkinter.CTkButton(master = root, text = "Download", bg_color="#004968",width=300, height=60, command=download)
button.place(relx=0.5, rely= 0.65, anchor = customtkinter.N)

text_box = customtkinter.CTkTextbox(root, bg_color="#004968" ,width=480,height=18, font=("Arial", 18))
text_box.place(relx=0.5, rely= 0.35, anchor = customtkinter.CENTER)

output_text = tk.Text(root, height=5, width=45, wrap=tk.WORD, font=("Arial", 18), bg="#004968")
output_text.place(relx=0.5, rely=0.51, anchor=tk.CENTER)

label = customtkinter.CTkLabel(root, text="Please, insert your link below", font=("Arial", 18), fg_color="#004968", corner_radius=2)
label.place(relx=0.3, rely=0.273, anchor=tk.CENTER)

root.mainloop()



