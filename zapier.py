import requests
import json

def send_response(url, update):
    if(url is None): return None
    text = update.message.text
    payload = { 'question': { 'user': update.message.from_user.username, 'response': text } }
    requests.post(url, data=json.dumps(payload))

def send_audio(url, username, telegram_url):
    if(url is None): return None

    payload = { 'question': { 'user': username, 'response': telegram_url } }
    requests.post(url, data=json.dumps(payload))
