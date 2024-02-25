import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import dotenv
import webbrowser

from flask import Flask, redirect, session, url_for
dotenv.load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
#redirect_uri = "https://127.0.0.1:8080/callback"

app = Flask(__name__)
app.secret_key = 'dfhkdsjhfdskjkasdf'

@app.route("/")
def home():
    auth_url = create_auth().get_authorize_url()

@app.route("/about")
def about():
    return "This is the about page."

if __name__ == "__main__":
    app.run(debug=True)


def create_auth():
    scope= 'user-library-read playlist-modify-public playlist-modify-private'
    username = '31tmrxnxrdyyiuuay4cquq6dzpty'
    redirect_url = url_for('redirect')
    token = SpotifyOAuth(scope=scope, username=username,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    #spotipyObj = spotipy.Spotify(auth_manager=token)
    return token



token = SpotifyOAuth(scope=scope, username=username,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
spotipyObj = spotipy.Spotify(auth_manager=token)
print("URL:", (token.get_authorize_url()))
url_ = token.get_authorize_url()


#create the playlist
playist_name= input("Enter a name for your new playlist: ")
playist_description = input("Enter a description for your new playlist: ")


spotipyObj.user_playlist_create(user=username,name=playist_name,public=True, description=playist_description)

# user_input = input("enter the song: ")
# list_of_songs = []

# while user_input != 'quit':
#     result = spotipyObj.search(q=user_input)
#     print(json.dumps(result,sort_keys=4,indent=4))
#     user_input = input("Enter the song: ")
