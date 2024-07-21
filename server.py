from flask import Flask, jsonify, send_file, render_template
from spotify_api import get_playlist, save_playlist_to_csv

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_playlist/<playlist_id>')
def get_playlist_route(playlist_id):
    tracks = get_playlist(playlist_id)
    return jsonify(tracks)

@app.route('/download_csv/<playlist_id>')
def download_csv_route(playlist_id):
    tracks = get_playlist(playlist_id)
    filename = f"{playlist_id}.csv"
    save_playlist_to_csv(tracks, filename)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
