import subprocess
import tkinter as tk
import threading
import os
import sys
import random

# This program is high-key vibe coded
cookies = False
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

if os.path.exists("cookies.txt"):
    cookies = True
    print("Cookies found:", cookies)
else:
    print("No cookies found.")

# Start threading to avoid blocking the GUI
yt_dlp_ready = threading.Event()

def update_yt_dlp():
    subprocess.run(["pip", "install", "--upgrade", "yt-dlp"], check=True, creationflags=CREATE_NO_WINDOW)
    yt_dlp_ready.set()

# In start_download(), before starting the dl thread:
def start_download():
    url = entry.get()
    fmt = var.get()
    if not url:
        label.config(text="Please enter YouTube URL")
        return
    
    if not yt_dlp_ready.is_set():
        label.config(text="Still updating yt-dlp, please wait...")
        return

    thread = threading.Thread(target=dl, args=(url, fmt, label), daemon=True)
    thread.start()

# Function to handle the download process
def dl(url, fmt, label):
    global cookies

    label.config(text="Starting download...")

    # Choosing the command based on the format and cookies existence
    if cookies:
        if fmt == "mp3":
            print("cookies found, downloading audio")
            command = [
                "yt-dlp",
                "--format", "bestaudio/best",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "320",
                "--cookies", "cookies.txt",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
        elif fmt == "mp4":
            print("cookies found, downloading video")
            command = [
                "yt-dlp",
                "--format", "bestvideo+bestaudio/best",
                "--cookies", "cookies.txt",
                "--merge-output-format", "mp4",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
        elif fmt == "webm":
            print("cookies found, downloading video")
            command = [
                "yt-dlp",
                "--format", "bestvideo+bestaudio/best",
                "--cookies", "cookies.txt",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
    else:
        if fmt == "mp3":
            command = [
                "yt-dlp",
                "--format", "bestaudio/best",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "320",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
        elif fmt == "mp4":
            command = [
                "yt-dlp",
                "--format", "bestvideo+bestaudio/best",
                "--merge-output-format", "mp4",
                "-o", "downloads/%(title)s.%(ext)s",
                "--audio-format", "aac",
                "--postprocessor-args", "ffmpeg:-c:v copy -c:a aac -b:a 192k",
                url
            ]
        elif fmt == "webm":
            command = [
                "yt-dlp",
                "--format", "bestvideo+bestaudio/best",
                "--merge-output-format", "webm",
                "--audio-format", "aac",
                "--postprocessor-args", "ffmpeg:-c:v copy -c:a aac -b:a 192k",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
    if command is None:  # ← guard before running
        label.config(text=f"Unknown format: {format}")
        return

    # Output success or error message
    try:
        print(fmt)
        subprocess.run(command, check=True, creationflags=CREATE_NO_WINDOW)
        print("Download has been finished")
        if random.random() < 0.01:
            label.config(text="🗣️🔥 SIGMA DOWNLOAD COMPLETE FR FR NO CAP 🔥🗣️")
        else:
            label.config(text="Download finished.")
    except subprocess.CalledProcessError as err:
        label.config(text=f"Error: {err}")

# GUI
if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    threading.Thread(target=update_yt_dlp, daemon=True).start()

    root = tk.Tk()
    root.title("YouTube Downloader 2001")
    root.geometry("600x350")

    entry = tk.Entry(root, width=50)
    entry.pack(pady=10)
    entry.focus_set()

    var = tk.StringVar(value="mp4")

    frame = tk.Frame(root)
    frame.pack()

    radio_audio = tk.Radiobutton(frame, text="Audio (MP3)", variable=var, value="mp3")
    radio_audio.pack(side="left", padx=10)

    radio_video = tk.Radiobutton(frame, text="Video (MP4)", variable=var, value="mp4")
    radio_video.pack(side="left", padx=10)

    radio_webm = tk.Radiobutton(frame, text="Video (WEBM)", variable=var, value="webm")
    radio_webm.pack(side="left", padx=10)

    button = tk.Button(root, text="Download", width=20, height=2, command=start_download)
    button.pack(pady=10)

    label = tk.Label(root, text="Enter a YouTube video/playlist URL")
    label.pack(pady=10)

    root.mainloop()
