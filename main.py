from flask import Flask,request, render_template, flash,url_for,redirect,send_file, session
from pytube import YouTube
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Instinct'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['GET','POST'])
def get_video():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
        except:
            return render_template("home.html", error = True)

        return render_template("home.html", url = url)


@app.route('/download', methods=['GET','POST'])
def download():
    filepath = ""
    if request.method == 'POST':
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        filepath = video.download("static/")
        return send_file(filepath, as_attachment=True)
    
    os.remove(filepath)
    return redirect(url_for('home'))

if __name__ == "__main__":
	app.run(debug=False)