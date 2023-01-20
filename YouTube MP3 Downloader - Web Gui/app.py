import os
from flask import Flask, request, render_template, send_file, redirect, url_for
from src.downloader import YouTubeMp3Downloader
# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function

@app.route('/')
def home():
   return redirect('/home')

@app.route('/home', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       url = request.form.get("url", None)
       if url[:23] != "https://www.youtube.com":
          print("wrong url")
          return render_template('index.html')
       song = request.form.get("song")
       artist = request.form.get("artist")
       
       
       if url=="" or song=="" or artist=="":
          print("No data in Form")
          return render_template('index.html')
       else: 
         audio_file_name = f"{song} - {artist}"
         print("Audio File Name: ", audio_file_name)
         obj = YouTubeMp3Downloader(url_link=url, name=audio_file_name)
         obj.download()
         audio_file = f"content/{audio_file_name}.mp3"
         return send_file(audio_file, as_attachment=True), os.remove(audio_file)
         
    return render_template('index.html')



if __name__=='__main__':
   app.run(port=5000, debug=True)
