import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

URL = "https://www.billboard.com/charts/hot-100/2000-08-12/"

response = requests.get(URL)

website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

# music_title =soup.find_all(name="h3", id="title-of-a-story")
music_title =soup.select(selector="li .o-chart-results-list__item #title-of-a-story")
# print(music_title)

music_list = [(music.getText()).strip() for music in music_title]
print(music_list)

date = input("Which year do you want to travel to? Type the date in this format YYY-MM-DD: ")

client_id = "1e95363bb9734aa8a27c5c1ee36eedf5"
client_secret = "ae9687262dc149768a5c845aba9c4608"
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://example.com",
                                               scope=scope,
                                               show_dialog=True,
                                               cache_path="token.txt"))

song_uris = []
# year = date.split("-")[0]


for song in music_list:
    result = sp.search(q=f"{song} {date}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(song_uris)
user_id = sp.current_user()["id"]
print(user_id)
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100",public=False )
print(playlist["id"])
add_song = sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(add_song)

#######################################################################################################

urn = 'q:track:Try Again,year:%@2000'
track = "Try Again"
years = 1999-2000

# query = f"{track} {year}"


# pprint(track)

# artist = 'BROODS'
# track = 'Couldn’t Believe'
# album = 'Conscious'
# query = f'{track} {artist} {album}'
# track_info = sp.search(q=query, type='track', limit=25)
# pprint(track_info)