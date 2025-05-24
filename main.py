import subprocess
import tkinter as tk
import threading
import os


cookies = False

if os.path.exists("cookies.txt"):
    cookies = True

print("Cookies found:", cookies)

# Start threading to avoid blocking the GUI
def start_download():
    url = entry.get()
    mode = var.get()

    thread = threading.Thread(target=dl, args=(url, mode, label), daemon=True)
    thread.start()

# Function to handle the download process
def dl(url, mode, label):
    global cookies
    label.config(text="Starting download...")

    # Choosing the command based on the mode and cookies existence
    if cookies:
        if mode == "audio":
            print("cookies found, downloading audio")
            command = [
                "yt-dlp",
                "--format", "bestaudio/best",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "320K",
                "--cookies", "cookies.txt",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
        else:
            command = [
                "yt-dlp",
                "--format", "bestvideo+bestaudio/best",
                "--cookies", "cookies.txt",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
    else:
        if mode == "audio":
            command = [
                "yt-dlp",
                "--format", "bestaudio/best",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "320K",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]
        else:
            command = [
                "yt-dlp",
                "--format", "bestvideo+bestaudio/best",
                "-o", "downloads/%(title)s.%(ext)s",
                url
            ]

    # Output success or error message
    try:
        subprocess.run(command, check=True)
        label.config(text="Download finished.")
    except subprocess.CalledProcessError as err:
        label.config(text=f"Ошибка: {err}")

# GUI
root = tk.Tk()
root.title("YouTube Downloader 2000")
root.geometry("600x350")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)
entry.focus_set()

var = tk.StringVar(value="audio")

frame = tk.Frame(root)
frame.pack()

radio_audio = tk.Radiobutton(frame, text="Audio (MP3)", variable=var, value="audio")
radio_audio.pack(side="left", padx=10)

radio_video = tk.Radiobutton(frame, text="Video (MP4)", variable=var, value="video")
radio_video.pack(side="left", padx=10)

button = tk.Button(root, text="Download", width=20, height=2, command=start_download)
button.pack(pady=10)

label = tk.Label(root, text="Enter a YouTube video/playlist URL")
label.pack(pady=10)

root.mainloop()
