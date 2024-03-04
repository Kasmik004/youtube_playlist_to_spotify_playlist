from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import json
import os
import dotenv
import webbrowser
import requests
from flask import session

dotenv.load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

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