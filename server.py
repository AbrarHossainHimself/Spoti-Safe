from flask import Flask, jsonify, send_file, session, redirect, url_for, render_template
from spotify_api import get_playlist, save_playlist_to_csv
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'test'
oauth = OAuth(app)

spotify = oauth.register(
    name='spotify',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize',
    redirect_uri='YOUR_REDIRECT_URI',
    client_kwargs={'scope': 'user-library-read playlist-read-private'}
)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return spotify.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = spotify.authorize_access_token()
    session['token'] = token
    return redirect('/profile')

@app.route('/profile')
def profile():
    token = session.get('token')
    resp = spotify.get('https://api.spotify.com/v1/me/playlists', token=token)
    return jsonify(resp.json())

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
