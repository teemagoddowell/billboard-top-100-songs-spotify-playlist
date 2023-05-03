import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIFY_CLIENT_ID = os.environ["SP_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SP_CLIENT_SECRET"]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]


user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{user_date}"

# Scrape Billboard
response = requests.get(URL)
data = response.text
soup = BeautifulSoup(data, "html.parser")
top_100_songs = soup.select(selector="li h3", class_="c-title")
song_list = []
song_url = []

# Top 100 Songs List
for song in top_100_songs:
    song_list.append(song.getText().strip())
    if len(song_list) > 99:
        break

# Search for songs on Spotify
for song in song_list:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        url = result["tracks"]["items"][0]["uri"]
        song_url.append(url)
    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped")

# Create New Playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_url)
