from pytube import YouTube
import ssl
from moviepy.editor import *
from moviepy.audio.io.AudioFileClip import AudioFileClip
from os import listdir
from os.path import isfile, join
import urllib.request
class YouTubeMp3Downloader:
    def __init__(self, url_link: str, name: str, ) -> None:
        
        self.url_link = url_link
        self.name = name
        
    def download(self):
        """
            download mp4 file from youtube 
            mp4 file will be stored in video folder
            mp4 file will be converted into mp3 and stored in music with self.name
        """
        # download file mp4
        ssl._create_default_https_context = ssl._create_unverified_context
        youtubeObj = YouTube(self.url_link)
        youtubeObj = youtubeObj.streams.get_audio_only()
        youtubeObj.download("audio_content")
        
        # download the thumbnail
        youtubeObj = YouTube(self.url_link)
        thumbnail_url = youtubeObj.thumbnail_url
        urllib.request.urlretrieve(thumbnail_url, "thumbnail.jpg")
        
        # convert to mp3        
        # get the mp4 file name in the /video folder
        mypath = "audio_content"
        mp4_file_name = [f for f in listdir(mypath) if isfile(join(mypath, f))][0]
        
        mp4_file_location = f"audio_content/{mp4_file_name}"
        mp3_file = f"audio_content/{self.name}.mp3"
        
        # Convert to mp3
        videoClip = AudioFileClip(mp4_file_location)
        videoClip.write_audiofile(mp3_file, bitrate = "192k")
        videoClip.close()
        
        # Delte MP4 file
        os.remove(mp4_file_location)
        