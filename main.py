import os
import sys
import time
import threading
import customtkinter
from pytubefix import Playlist, YouTube
from moviepy import VideoFileClip

# ----------------------- CONTROL FLAGS -----------------------
is_paused = False
is_stopped = False


# ----------------------- FUNCTIONALITY -----------------------

def download():
    global is_paused, is_stopped

    playlist_link = text_box.get(1.0, "end-1c").strip()
    if not playlist_link:
        status_message.configure(text="Error: Enter playlist link!", text_color="#FF3B3B")
        return

    selected_mode = format_var.get()
    if not selected_mode:
        status_message.configure(text="Error: Select a download format (MP3 or MP4)!", text_color="#FF3B3B")
        return

    status_message.configure(text_color="#e6e6e6")
    is_paused = False
    is_stopped = False
    
    target_text = selected_mode.split()[0] 
    status_message.configure(text=f"Starting {target_text} download...")
    progressbar.set(0)

    progressbar.place(relx=0.5, rely=0.75, anchor="center")
    download_button.place_forget()
    pause_button.place(relx=0.22, rely=0.88, anchor="center")
    stop_button.place(relx=0.78, rely=0.88, anchor="center")
    resume_button.place_forget()

    threading.Thread(target=download_playlist, args=(playlist_link, selected_mode)).start()


def download_playlist(playlist_link, mode):
    global is_paused, is_stopped

    target_format = "mp3" if "MP3" in mode else "mp4"

    try:
        playlist = Playlist(playlist_link)
        # If MP3, we have 2 steps (download + convert). If MP4, just 1.
        steps_per_video = 2 if target_format == "mp3" else 1
        total_steps = len(playlist.video_urls) * steps_per_video
        step = 0
    except Exception:
        safe_output("Error: Invalid playlist link", is_error=True)
        reset_ui_after_stop()
        return

    # 1. DOWNLOAD PHASE (Always downloads MP4 first)
    for link in playlist:

        if is_stopped:
            reset_ui_after_stop()
            return

        while is_paused:
            safe_output("Paused…")
            time.sleep(0.5)

        try:
            yt = YouTube(link)
            stream = yt.streams.filter(mime_type="video/mp4", progressive=False).first()
            if not stream:
                stream = yt.streams.filter(file_extension='mp4').first()
            
            name = yt.title
            stream.download("./Songs")

            safe_output(f"{name[:25]}... downloaded (Video)")

            step += 1
            update_progress(step / total_steps)

        except Exception as e:
            safe_output(f"Error downloading: {str(e)[:20]}", is_error=True)

    # 2. DECISION PHASE
    if target_format == "mp4":
        safe_output("Ready ✓ All videos downloaded!")
        finish_ui()
        return

    # 3. CONVERSION PHASE (Only if MP3 was selected)
    for file in os.listdir("./Songs"):

        if is_stopped:
            reset_ui_after_stop()
            return

        while is_paused:
            safe_output("Paused…")
            time.sleep(0.5)

        if file.endswith(".mp4"):
            try:
                full_path_mp4 = os.path.join("./Songs", file)
                full_path_mp3 = os.path.join("./Songs", file[:-4] + ".mp3")

                video_clip = VideoFileClip(full_path_mp4)
                audio_clip = video_clip.audio
                
                audio_clip.write_audiofile(full_path_mp3, logger=None)
                
                audio_clip.close()
                video_clip.close()

                safe_output(f"{file[:25]}... converted to MP3")
                
                os.remove(full_path_mp4)

                step += 1
                update_progress(step / total_steps)
            
            except Exception as e:
                safe_output(f"Conversion Error: {str(e)[:15]}", is_error=True)

    safe_output("Ready ✓ All songs downloaded!")
    finish_ui()


def reset_ui_after_stop():
    safe_output("Stopped by user.")
    finish_ui()


def finish_ui():
    root.after(0, lambda: _restore_buttons())


def _restore_buttons():
    progressbar.place_forget()
    pause_button.place_forget()
    resume_button.place_forget()
    stop_button.place_forget()
    download_button.place(relx=0.5, rely=0.75, anchor="center")


def safe_output(message, is_error=False):
    color = "#FF3B3B" if is_error else "#e6e6e6"
    root.after(0, lambda: status_message.configure(text=message, text_color=color))


def update_progress(value):
    root.after(0, lambda: progressbar.set(value))


# ----------------------- PAUSE / RESUME / STOP -----------------------

def pause_download():
    global is_paused
    is_paused = True
    pause_button.place_forget()
    resume_button.place(relx=0.22, rely=0.88, anchor="center")


def resume_download():
    global is_paused
    is_paused = False
    safe_output("Resuming…")
    resume_button.place_forget()
    pause_button.place(relx=0.22, rely=0.88, anchor="center")


def stop_download():
    global is_stopped
    is_stopped = True
    safe_output("Stopping…")


# ----------------------- SETUP -----------------------

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SONGS_DIR = os.path.join(BASE_DIR, "Songs")

if not os.path.exists(SONGS_DIR):
    os.makedirs(SONGS_DIR)


# ----------------------- UI CONFIGURATION -----------------------

customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()
root.title("Play.listed Downloader")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg="#121212") 


# ----------------------- HEADER -----------------------

title_frame = customtkinter.CTkFrame(
    root,
    fg_color="transparent",
    width=700,
    height=80
)
title_frame.place(relx=0.5, rely=0.10, anchor="center")

title = customtkinter.CTkLabel(
    title_frame,
    text="Play.listed",
    font=("Segoe UI", 46, "bold"),
    text_color="white",
    fg_color="transparent"
)
title.pack()

subtitle = customtkinter.CTkLabel(
    title_frame,
    text="© Adelin Prelipcean — YouTube Playlist Downloader",
    font=("Segoe UI", 16),
    text_color="#bbbbbb",
    fg_color="transparent"
)
subtitle.pack()


# ----------------------- MAIN CARD -----------------------

card = customtkinter.CTkFrame(
    root,
    width=550,
    height=400,
    corner_radius=12,
    fg_color="#1E1E1E"
)
card.place(relx=0.5, rely=0.55, anchor="center")

# Label
label2 = customtkinter.CTkLabel(
    card,
    text="Insert your playlist link:",
    font=("Segoe UI", 17),
    text_color="white"
)
label2.place(relx=0.5, rely=0.12, anchor="center")

# Textbox
text_box = customtkinter.CTkTextbox(
    card,
    width=480,
    height=40,
    corner_radius=8,
    fg_color="#0F0F0F",
    text_color="white",
    border_color="#FF3B3B",
    border_width=2,
    font=("Segoe UI", 15)
)
text_box.place(relx=0.5, rely=0.28, anchor="center")

# Format Selector
format_var = customtkinter.StringVar(value="") 

format_switch = customtkinter.CTkSegmentedButton(
    card,
    values=["MP3 (Audio)", "MP4 (Video)"],
    variable=format_var,
    width=200,
    height=30,
    corner_radius=15,
    selected_color="#FF3B3B",
    selected_hover_color="#CC2E2E",
    unselected_color="#333333",
    unselected_hover_color="#444444",
    font=("Segoe UI Semibold", 14)
)
format_switch.place(relx=0.5, rely=0.48, anchor="center")

# Status Message
status_message = customtkinter.CTkLabel(
    card,
    text="Waiting for playlist link...",
    width=480,
    height=35,
    corner_radius=8,
    fg_color="#181818",
    text_color="#e6e6e6",
    font=("Segoe UI", 15),
    anchor="w",
    padx=12
)
status_message.place(relx=0.5, rely=0.62, anchor="center")

# Progress Bar
progressbar = customtkinter.CTkProgressBar(
    card,
    width=480,
    height=15,
    corner_radius=5,
    progress_color="#FF3B3B",
    fg_color="#2a2a2a"
)
progressbar.set(0)
progressbar.place_forget()


# ----------------------- CONTROLS -----------------------

download_button = customtkinter.CTkButton(
    card,
    text="Download",
    width=300,
    height=50,
    corner_radius=25,
    fg_color="#FF3B3B",
    hover_color="#CC2E2E",
    font=("Segoe UI Semibold", 20),
    command=download
)
download_button.place(relx=0.5, rely=0.78, anchor="center")


pause_button = customtkinter.CTkButton(
    card,
    text="Pause",
    width=150,
    height=40,
    corner_radius=20,
    fg_color="#444444",
    hover_color="#333333",
    font=("Segoe UI Semibold", 16),
    command=pause_download
)
pause_button.place_forget()

resume_button = customtkinter.CTkButton(
    card,
    text="Resume",
    width=150,
    height=40,
    corner_radius=20,
    fg_color="#1F8BFF",
    hover_color="#166FCC",
    font=("Segoe UI Semibold", 16),
    command=resume_download
)
resume_button.place_forget()

stop_button = customtkinter.CTkButton(
    card,
    text="Stop",
    width=150,
    height=40,
    corner_radius=20,
    fg_color="#FF3B3B",
    hover_color="#CC2E2E",
    font=("Segoe UI Semibold", 16),
    command=stop_download
)
stop_button.place_forget()


root.mainloop()