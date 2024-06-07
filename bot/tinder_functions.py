import json
import requests

def post_tinder_api_request(url,api_token):
    response = requests.post(url, headers={"x-auth-token": api_token})
    return json.loads(response.text)

def get_tinder_api_request(url,api_token):
    response = requests.get(url, headers={"x-auth-token": api_token})
    return json.loads(response.text)