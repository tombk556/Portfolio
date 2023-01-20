from flask import Blueprint, render_template, request, flash, redirect, send_file
from flask_login import login_required, current_user
from .models import Note
from . import db
import os
from src.downloader import YouTubeMp3Downloader
from src.changeMetaData import ChangeMetaData
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        url_ = request.form.get('url')
        name_ = request.form.get('name')
        artist_ = request.form.get('artist')
        if url_ == "" or name_ == "" or artist_ == "":
            flash('Please fill out the entire form.', category='error')
        elif url_[:23] != "https://www.youtube.com":
            flash("Wrong url.", category='error')
        else:
            new_note = Note(url=url_, name=name_, artist=artist_,
                            user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template('home.html', user=current_user)



@views.route('/process', methods=['POST'])
def process():
    url = request.form['col1']
    name = request.form['col2']
    artist = request.form['col3']
    audio_file_name = f"{name} - {artist}"
    obj = YouTubeMp3Downloader(url_link=url, name=audio_file_name)
    obj.download()
    audio_file = f"./audio_content/{audio_file_name}.mp3"
    ChangeMetaData(audiofile = audio_file).change(title=name, artist=artist)
    audio_file = f"../audio_content/{audio_file_name}.mp3" 
    return send_file(audio_file, as_attachment=True), os.remove(f'audio_content/{audio_file_name}.mp3'), os.remove('./thumbnail.jpg')


@views.route('/delte', methods=['POST'])
def delte():
    id = request.form['col0']
    note = Note.query.get(id)
    print(note)
    print(current_user.id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return redirect('/')
