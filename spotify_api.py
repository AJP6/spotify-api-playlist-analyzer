from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter


load_dotenv()

limit = 10

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    redirect_uri = "http://127.0.0.1:8888/callback",
    scope = "user-top-read"
))

def get_top_artists(time_range):
    return sp.current_user_top_artists(limit=limit, time_range=time_range)

def get_top_tracks(time_range):
    return sp.current_user_top_tracks(limit=limit, time_range=time_range)

def get_user_genres(top_artists):
    genres = []
    for artist in top_artists['items']:
        genres.extend(artist['genres'])
    return list(set(genres))

def analyze_playlist_genres():
    playlists = sp.current_user_playlists()
    print("Choose a playlist:")
    for idx, playlist in enumerate(playlists['items'], start=1):
        number_of_tracks = playlist['tracks']['total']
        print(f"{idx}. {playlist['name']} ({number_of_tracks} tracks)")
    
    user_choice = int(input("Enter playlist number: ")) - 1
    selected_playlist = playlists['items'][user_choice]
    selected_playlist_id = selected_playlist['id']

    print(f"\nAnalyzing: {selected_playlist['name']}...")

    tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(selected_playlist_id, offset=offset)
        tracks.extend(response['items'])
        if response['next'] is None:
            break
        offset += len(response['items'])

    artist_ids = set()
    for item in tracks:
        track = item.get('track')
        if not track:
            continue
        for artist in track.get('artists', []):
            artist_ids.add(artist['id'])

    genre_counter = Counter()
    artist_ids = list(artist_ids)
    batch_size = 50 # max 50 at a time cause thats what spotify allows
    for i in range(0, len(artist_ids), batch_size):
        batch = [aid for aid in artist_ids[i:i+batch_size] if aid is not None]
        if not batch:
            continue
        artists = sp.artists(batch)['artists']
        for artist in artists:
            genre_counter.update(artist['genres'])
    
    if len(genre_counter) is 0:
        print("No tracks in this playlist")
        exit()

    print("\nTop Genres in Playlist:")
    for genre, count in genre_counter.most_common(20):
        print(f"{genre}: {count}")
