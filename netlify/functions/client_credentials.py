import base64
import requests

client_id = '7d920b2e3be9402ba85d5641cae2f7f1'
client_secret = '76d184f228d845d8802d93c80613dbfd'

def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
    }
    payload = {'grant_type': 'client_credentials'}
    
    response = requests.post(auth_url, headers=headers, data=payload)
    response_data = response.json()
    return response_data['access_token']

# Test authentication
if __name__ == "__main__":
    token = get_access_token()
    print(f"Access Token: {token}")
    
