import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

playlist_code = "https://open.spotify.com/playlist/1gd8rPLzo3bjk1yyQce0h7?si=c228ee05bd8c4e3c"
playlist_dict = sp.playlist(playlist_code)

no_of_songs = playlist_dict["tracks"]["total"]

album_list = []
song_list = []
release_date_list = []
artists_list = []

tracks = playlist_dict['tracks']
items = tracks['items']
offset = 0

i=0
while i < no_of_songs:
    song = items[i-offset]['track']['name']
    album = items[i-offset]['track']['album']['name']
    release_date = items[i-offset]['track']['album']['release_date']
    artists = [k['name'] for k in items[i-offset]['track']['artists']]
    artists = ','.join(artists)
    album_list.append(album)
    song_list.append(song)
    release_date_list.append(release_date)
    artists_list.append(artists)

    if (i+1)%100 == 0:
        tracks = sp.next(tracks)
        items = tracks['items']
        offset = i+1
    i+=1

final_data = list(zip(song_list, artists_list, album_list, release_date_list))

import csv
Details = ['Name', 'Artists', 'Album', 'Release_Date']
rows = final_data
with open("sad_songs.csv", 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(Details)
    write.writerows(rows)

f.close()