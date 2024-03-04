
import requests
import youtube_title_parse
api_key = 'AIzaSyDtOr1WM1s2X5oy_RmULTQGUdPL0L4PzK8'
playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
prams = {
    'key' : api_key,
    'part' : "snippet",
    'maxResults':  10,
    'playlistId' : "PLUWT5vnZ7a39uMBO5bPkTtjxW8f_RY0Ti"
    }

results = requests.get(playlist_url, params=prams)

titles = []
for result in results.json()['items']:
    titles.append(result['snippet']['title'])

art =[]
song =[]
for t in titles:
    temp_a, temp_b = youtube_title_parse.get_artist_title(t)
    art.append(temp_a)
    song.append(temp_b)

for s in art:
    print(s)