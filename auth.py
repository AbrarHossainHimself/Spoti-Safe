from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'test'
oauth = OAuth(app)

spotify = oauth.register(
    name='spotify',

    client_id='',
    client_secret='',


    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize',
    authorize_params=None,
    redirect_uri='http://localhost:5000/callback',
    client_kwargs={'scope': 'user-library-read playlist-read-private'}
)

@app.route('/')
def homepage():
    return 'Welcome to the Spotify Backup Tool!'

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
    return resp.json()

if __name__ == "__main__":
    app.run(debug=True)
