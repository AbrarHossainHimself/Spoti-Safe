import requests
import json
from client_credentials import get_access_token


import csv

def get_playlist(playlist_id):
    token = get_access_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(url, headers=headers)
    playlist_data = response.json()
    
    tracks = []
    for item in playlist_data['tracks']['items']:
        track = item['track']
        track_info = {
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'track_name': track['name']
        }
        tracks.append(track_info)
    
    return tracks


def save_playlist_to_csv(tracks, filename):
    keys = tracks[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tracks)

# Test saving playlist to CSV
if __name__ == "__main__":
    playlist_id = '7GBcBrxbMkoFon8v7RGxrA?si=ad54bdb8efde4ee5'
    tracks = get_playlist(playlist_id)
    save_playlist_to_csv(tracks, f"{playlist_id}.csv")
