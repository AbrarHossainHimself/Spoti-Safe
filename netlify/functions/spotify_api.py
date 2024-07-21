import requests
import csv
from client_credentials import get_access_token

def get_playlist(playlist_id):
    token = get_access_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'limit': 100,
        'offset': 0
    }
    
    tracks = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        playlist_data = response.json()
        
        for item in playlist_data['items']:
            track = item['track']
            if track:  # Ensure there is track information
                track_info = {
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'track_name': track['name']
                }
                tracks.append(track_info)
        
        url = playlist_data['next']  # Get the next page URL
        params = {}  # reset params as `next` already contains the pagination parameters
    
    return tracks

def save_playlist_to_csv(tracks, filename):
    if not tracks:
        return  # Handle empty track list
    keys = tracks[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tracks)

# Test fetching all tracks from a playlist
if __name__ == "__main__":
    playlist_id = 'YOUR_PLAYLIST_ID'
    tracks = get_playlist(playlist_id)
    save_playlist_to_csv(tracks, f"{playlist_id}.csv")
