from pytube import YouTube
import ssl
from moviepy.editor import *
from os import listdir
from os.path import isfile, join

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
        youtubeObj = youtubeObj.streams.get_highest_resolution()
        youtubeObj.download("content")
        
        # convert to mp3        
        # get the mp4 file name in the /video folder
        mypath = "content"
        mp4_file_name = [f for f in listdir(mypath) if isfile(join(mypath, f))][0]
        
        mp4_file_location = f"content/{mp4_file_name}"
        mp3_file = f"content/{self.name}.mp3"
        
        # Convert to mp3
        videoClip = VideoFileClip(mp4_file_location)
        audioClip = videoClip.audio
        audioClip.write_audiofile(mp3_file, fps=44100, bitrate='3000k')
        
        audioClip.close()
        videoClip.close()
        
        # Delte MP4 file
        os.remove(mp4_file_location)	
        