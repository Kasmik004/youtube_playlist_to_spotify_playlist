
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import json
import os
import dotenv
import webbrowser

from flask import Flask, redirect, session, url_for, request
dotenv.load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = 'http://127.0.0.1:5000/callback'

# app = Flask(__name__)
# app.secret_key = 'dfhkdsjhfdskjkasdf'

# @app.route("/")
# def home():
#     auth_url = create_auth().get_authorize_url()
#     return redirect(auth_url)

# @app.route("/redirect")
# def redirect():
#     session.clear
#     code = request.args.get('code')
#     token_info = create_auth().get_access_token(code)
#     session['TOKEN_INFO'] = token_info
#     return redirect(url_for('save'), external=True)    

# if __name__ == "__main__":
#     app.run(debug=True)


# def create_auth():
#     scope= 'user-library-read, playlist-modify-public, playlist-modify-private'
#     username = '31tmrxnxrdyyiuuay4cquq6dzpty'
#     redirect_url = url_for('redirect')
#     token = SpotifyOAuth(scope=scope, username=username,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_url)
#     #spotipyObj = spotipy.Spotify(auth_manager=token)
#     return token

# def get_token():
#     token_info = session.get('TOKEN_INFO', None)
#     if not token_info:
#         return redirect(url_for('hone',external=False))
    
#     now = int(time.time())
#     is_expired = get_token['expires_in'] - now <60
#     if(is_expired): 
#         spotify_oauth = create_spotify_oauth()


# token = SpotifyOAuth(scope=scope, username=username,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
# spotipyObj = spotipy.Spotify(auth_manager=token)
# print("URL:", (token.get_authorize_url()))
# url_ = token.get_authorize_url()


# #create the playlist
# playist_name= input("Enter a name for your new playlist: ")
# playist_description = input("Enter a description for your new playlist: ")


# spotipyObj.user_playlist_create(user=username,name=playist_name,public=True, description=playist_description)

# # user_input = input("enter the song: ")
# # list_of_songs = []

# # while user_input != 'quit':
# #     result = spotipyObj.search(q=user_input)
# #     print(json.dumps(result,sort_keys=4,indent=4))
# #     user_input = input("Enter the song: ")

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

@app.route('/')
def home():
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
    
    playlist = sp.current_user_playlists()
    playlist_list = [(pl['name'],pl['external_urls']['spotify']) for pl in playlist['items']]
    playlist_html = '<br'.join([f'{name}: {url}' for name,url in playlist_list])
    return playlist_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
    



if __name__ == '__main__':
    app.run(debug=True)



