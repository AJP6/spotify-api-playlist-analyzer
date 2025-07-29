from spotify_api import *

def main():
    print("Choose what data you want:")
    print("1. Top Artists")
    print("2. Top Tracks")
    print("3. Top Genres")
    print("4. Analyze Playlist Genres")

    choice = input("Enter choice (1-4): ")

    if not choice == "4":
        print("\nChoose time range:")
        print("short_term - last 4 weeks")
        print("medium_term - last 6 months")
        print("long_term - several years")

        time_range = input("Enter time range: ").strip()

    if choice == "1":
        artists = get_top_artists(time_range=time_range)
        print("\nYour Top Artists:")
        for idx, artist in enumerate(artists['items'], start=1):
            print(f"{idx}. {artist['name']}")
    elif choice == "2":
        tracks = get_top_tracks(time_range=time_range)
        print("\nYour Top Tracks:")
        for idx, track in enumerate(tracks['items'], start=1):
            print(f"{idx}. {track['name']} - {track['artists'][0]['name']}")
    elif choice == "3":
        artists = get_top_artists(time_range=time_range)
        genres = get_user_genres(artists)
        print("\nYour Top Genres:")
        for genre in genres:
            print(genre)
    elif choice == "4":
        analyze_playlist_genres()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()