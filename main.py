import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date[:4]

#Scraping Billboard 100
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)

billboard_web_page = response.text
soup = BeautifulSoup(billboard_web_page, "html.parser")

all_songs = soup.find_all(name="h3", class_="c-title")

song_titles = [song.getText().strip() for song in all_songs]

print(song_titles)

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=YOUR SPOTIFY ID HERE,
        client_secret=YOUR SPOTIFY SECRET HERE,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []

for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(song_uris)

#Creating a new private playlist in Spotify

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

billboard = sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)