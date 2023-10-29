import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set your API keys
lastfm_api_key = '542bfbc2a64959eed5a6a2f1409d459a'
spotify_client_id = 'YOUR_SPOTIFY_CLIENT_ID'
spotify_client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'

lastfm_base_url = 'http://ws.audioscrobbler.com/2.0/'
lastfm_params = {
    'method': 'artist.getinfo',
    'format': 'json',
    'api_key': lastfm_api_key,
}

spotify_credentials = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(client_credentials_manager=spotify_credentials)


def get_artist_info(artist_name):
    lastfm_params['artist'] = artist_name
    response = requests.get(lastfm_base_url, params=lastfm_params)
    data = response.json()

    if 'artist' in data:
        artist = data['artist']
        name = artist['name']
        bio = artist['bio']['content'] if 'bio' in artist else 'No biography available.'
        print(f"Artist: {name}")
        print(f"Biography:\n{bio}\n")
    else:
        print("Sorry, I couldn't find information about this artist. Please try again.")


def recommend_songs(artist_name):
    results = sp.search(q=artist_name, type='artist', limit=1)

    if results and 'artists' in results and 'items' in results['artists']:
        artist_id = results['artists']['items'][0]['id']
        recommended_tracks = sp.recommendations(seed_artists=[artist_id], limit=5)

        print(f"Recommended songs by {artist_name}:\n")
        for i, track in enumerate(recommended_tracks['tracks'], 1):
            print(f"{i}. {track['name']} by {', '.join([a['name'] for a in track['artists']])}")
    else:
        print("Sorry, I couldn't find recommendations for songs by this artist. Please try again.")


if __name__ == "__main__":
    artist_name = input("Enter the name of a musical artist: ")

    get_artist_info(artist_name)
    recommend_songs(artist_name)
