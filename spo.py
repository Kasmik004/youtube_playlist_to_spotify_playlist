
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import json
import os
import dotenv
import webbrowser
import requests

from flask import Flask, redirect, session, url_for, request, render_template
dotenv.load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = 'http://127.0.0.1:5000/callback'


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
scope= 'user-library-read, playlist-modify-public, playlist-modify-private'


cache_handler = FlaskSessionCacheHandler(session=session)

auth_manager = SpotifyOAuth(
    scope=scope,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=auth_manager)


@app.route('/youtube')
def youtube():
    

    api_key = 'AIzaSyDtOr1WM1s2X5oy_RmULTQGUdPL0L4PzK8'
    playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    prams = {
        'key' : api_key,
        'part' : "snippet",
        'maxResults':  10,
        'playlistId' : "PLUWT5vnZ7a39F4DulEif3X3vCXRv6KqMt"
    }

    results = requests.get(playlist_url, params=prams)

    titles = []
    for result in results.json()['items']:
        titles.append(result['snippet']['title'])

    return titles




@app.route('/index')
def index():
    session['index'] = 1
    return render_template("index.html")

@app.route('/',methods=['GET','POST'])
def home():
    if 'index' not in session:
        return redirect(url_for('index'))

    session['playlist_name'] = request.form['name']
    session['playlist_description'] = request.form['des']
    cached_token = cache_handler.get_cached_token()
    if not auth_manager.validate_token(cached_token):
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    
    return redirect(url_for('get_playlists'))




@app.route('/callback')
def callback():
    auth_manager.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))


@app.route('/get_playlists')
def get_playlists():
    cached_token = cache_handler.get_cached_token()
    if not auth_manager.validate_token(cached_token):
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    
    username = sp.current_user()['id']
    # playist_name="default"
    # playist_description="default"
    
    # playist_name= session['playlist_name']
    # playist_description = session['playlist_description']
    

    #sp.user_playlist_create(user=username,name=playist_name,public=True, description=playist_description)
    #return "Success"
    
    playlist = sp.current_user_playlists()
    #return playlist
    playlist_list = [(pl['name'],pl['external_urls']['spotify']) for pl in playlist['items']]
    
    playlist_html = '<br>'.join([f'{name}: {url}' for name,url in playlist_list])
    return playlist_html

@app.route('/add_playlist')
def add_playlist():
    username = sp.current_user()
    playist_name= input("Enter a name for your new playlist: ")
    playist_description = input("Enter a description for your new playlist: ")
    return None

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
    



if __name__ == '__main__':
    app.run(debug=True)



