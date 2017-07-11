import requests
from slackbot_settings import API_AI_KEY

# Keep this, like, super secret, ya know?

def query(user_id, text):
    endpoint = 'https://api.api.ai/api/query'
    parameters = {
        'v': 20150910, # API version
        'query': text,
        'lang': 'en',
        'sessionId': user_id
    }
    headers = {
      'Authorization': 'Bearer ' + API_AI_KEY
    }
    response = requests.get(endpoint, params=parameters, headers=headers)
    return response.json()
