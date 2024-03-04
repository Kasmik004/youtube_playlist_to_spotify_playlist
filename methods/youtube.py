import requests
import youtube_title_parse
from models.model import sp

api_key = 'AIzaSyDtOr1WM1s2X5oy_RmULTQGUdPL0L4PzK8'
playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'

def get_songs(id):
    params = {
        'key': api_key,
        'part': "snippet",
        'maxResults': 10,
        'playlistId': id
    }

    results = requests.get(playlist_url, params=params)

    titles = []
    for result in results.json()['items']:
        titles.append(result['snippet']['title'])

    art = []
    song = []
    for t in titles:
        temp_a, temp_b = youtube_title_parse.get_artist_title(t)
        art.append(temp_a)
        song.append(temp_b)

    return art


def get_song_uris(songs):
    uris=[]
    for song in songs:
        try:
            
            result = sp.search(q=song)
            uris.append(result['tracks']['items'][0]['uri'])    
        except:
            print("NO data found for :",song)
            
    return uris


def get_playlist_id_from_url(url):
    split_list = url.split('=')
    return split_list[2]

CHECK=0


