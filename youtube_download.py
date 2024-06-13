from pytube import YouTube
import os
from moviepy.editor import *
from moviepy.audio.io.AudioFileClip import AudioFileClip
import tkinter as tk
from tkinter import filedialog

def download_video(link, path):
    try:
        yutub = YouTube(link)
        video_streams = yutub.streams.filter(file_extension='mp4', only_video=True).order_by('resolution').desc()
        audio_stream = yutub.streams.filter(only_audio=True).first()

        resolutions = [stream.resolution for stream in video_streams]
        unique_resolutions = list(dict.fromkeys(resolutions))

        print(f"Available resolutions for {yutub.title}:")
        for idx, resolution in enumerate(unique_resolutions):
            print(f"{idx + 1}: {resolution}")

        choice = int(input("Enter the number corresponding to your preferred resolution: "))
        selected_resolution = unique_resolutions[choice - 1]

        video_stream = video_streams.filter(res=selected_resolution).first()

        print(f"Downloading video: {yutub.title} at {selected_resolution}")
        video_path = video_stream.download(output_path=path, filename="video.mp4")

        print("Downloading audio...")
        audio_path = audio_stream.download(output_path=path, filename="audio.mp4")

        print("Combining video and audio...")
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(os.path.join(path, f"{yutub.title}.mp4"))

        video_clip.close()
        audio_clip.close()
        os.remove(video_path)
        os.remove(audio_path)

        print("Download and combination completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_audio(link, path):
    try:
        yutub = YouTube(link)
        ys = yutub.streams.filter(only_audio=True).first()

        print(f"Downloading: {yutub.title}")
        audio_file = ys.download(output_path=path)
        base, ext = os.path.splitext(audio_file)
        new_file = base + '.mp3'

        audio_clip = AudioFileClip(audio_file)
        audio_clip.write_audiofile(new_file)
        audio_clip.close()

        os.remove(audio_file)

        print("Download and conversion to MP3 completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    choice = input("Enter 1 to download as MP4 video or 2 to download as MP3 audio: ")
    link = input("Enter the YouTube video link: ")
    path = filedialog.askdirectory(title="Select the directory to save the file")

    if not path:
        print("No directory selected. Exiting...")
        exit()

    if choice == '1':
        download_video(link, path)
    elif choice == '2':
        download_audio(link, path)
    else:
        print("Invalid choice. Please enter 1 or 2.")
