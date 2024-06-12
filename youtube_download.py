from pytube import YouTube
import os
from moviepy.editor import *

def download_video(link, path):
    yutub = YouTube(link)
    ys = yutub.streams.get_highest_resolution()

    print(f"Downloading: {yutub.title}")
    ys.download(path)
    print("Download completed!")

def download_audio(link, path):
    yutub = YouTube(link)
    ys = yutub.streams.filter(only_audio=True).first()

    print(f"Downloading: {yutub.title}")
    audio_file = ys.download(output_path=path)
    base, ext = os.path.splitext(audio_file)
    new_file = base + '.mp3'

    # Convert to MP3
    audio_clip = AudioFileClip(audio_file)
    audio_clip.write_audiofile(new_file)
    audio_clip.close()

    # Remove the original audio file
    os.remove(audio_file)

    print("Download and conversion to MP3 completed!")

if __name__ == "__main__":
    choice = input("Enter 1 to download as MP4 video or 2 to download as MP3 audio: ")
    link = input("Enter the YouTube video link: ")
    path = input("Enter the path where the file will be saved: ")

    if not os.path.exists(path):
        os.makedirs(path)

    if choice == '1':
        download_video(link, path)
    elif choice == '2':
        download_audio(link, path)
    else:
        print("Invalid choice. Please enter 1 or 2.")
