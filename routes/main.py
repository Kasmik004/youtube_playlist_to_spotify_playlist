from flask import Blueprint, render_template, session, request, redirect, url_for, flash, sessions
import requests
from models.model import cache_handler, sp, auth_manager
from methods.youtube import get_song_uris, get_songs, get_playlist_id_from_url

from methods import youtube

main = Blueprint('main', __name__)


'''
@main.route('/youtube')
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
'''



@main.route('/index')
def index():
    youtube.CHECK = 1
    session['index'] = 1
    return render_template("index.html")

@main.route('/',methods=['GET','POST'])
def home():
    if 'index' not in session:
        return redirect(url_for('main.index'))
    
    
    session['playlist_name'] = request.form['name']
    session['playlist_description'] = request.form['des']
    session['play_id'] = request.form['id']
    cached_token = cache_handler.get_cached_token()
    if not auth_manager.validate_token(cached_token):
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    
    return redirect(url_for('main.get_playlists'))




@main.route('/callback')
def callback():
    if 'index' not in session:
        return redirect(url_for('main.index'))
    auth_manager.get_access_token(request.args['code'])
    return redirect(url_for('main.get_playlists'))


@main.route('/get_playlists')
def get_playlists():
    if 'index' not in session:
        return redirect(url_for('main.index'))
    cached_token = cache_handler.get_cached_token()
    if not auth_manager.validate_token(cached_token):
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    
    username = sp.current_user()['id']
    # playist_name="default"
    # playist_description="default"
    
    playist_name= session['playlist_name']
    playist_description = session['playlist_description']
    

    sp.user_playlist_create(user=username,name=playist_name,public=True, description=playist_description)
    youtube_playlist_id = session['play_id']  #this is actually the url of the video
    y_p_id = get_playlist_id_from_url(youtube_playlist_id)  #here we split the url into playlist id
    songs = get_songs(y_p_id)
    song_uri = get_song_uris(songs=songs)
    
    current_playlist = sp.user_playlists(user=username)
    c_p=current_playlist['items'][0]['id']
    sp.user_playlist_add_tracks(user=username,playlist_id=c_p,tracks=song_uri)
    
    
    return redirect(url_for('main.logout'))
    
    #playlist = sp.current_user_playlists()
    #return playlist
    #playlist_list = [(pl['name'],pl['external_urls']['spotify']) for pl in playlist['items']]
    
    #playlist_html = '<br>'.join([f'{name}: {url}' for name,url in playlist_list])
    #return playlist_html


#may come in use to add more features
@main.route('/add_playlist')
def add_playlist():
    if 'index' not in session:
        return redirect(url_for('main.index'))
    username = sp.current_user()
    playist_name= input("Enter a name for your new playlist: ")
    playist_description = input("Enter a description for your new playlist: ")
    return None

@main.route('/logout')
def logout():
    if 'index' not in session:
        return redirect(url_for('main.index'))
    session.clear()
    flash("Successfully added")
    return redirect(url_for('main.index'))