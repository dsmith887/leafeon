import requests
from config import API_KEY

ID_LOOKUP = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'

SUMMONER_LOOKUP = 'orchy'

payload = {'api_key': API_KEY}

r = requests.get(ID_LOOKUP + SUMMONER_LOOKUP, params=payload)

account_id = r.json()['accountId']