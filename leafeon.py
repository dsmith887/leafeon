import requests
import csv
from config import API_KEY

API_LOC = 'https://na1.api.riotgames.com'
ID_LOOKUP = '/lol/summoner/v4/summoners/by-name/'
MATCHLIST_LOOKUP = '/lol/match/v4/matchlists/by-account/'
MATCH_LOOKUP = '/lol/match/v4/matches/'

SUMMONER_LOOKUP = 'Das Toona Fish'

payload = {'api_key': API_KEY}

id_request = requests.get(API_LOC + ID_LOOKUP + SUMMONER_LOOKUP, params=payload)

account_id = id_request.json()['accountId']

match_request = requests.get(API_LOC + MATCHLIST_LOOKUP + account_id, params=payload)

matchlist = match_request.json()['matches']

games = []

for match in matchlist:
    games.append({'game_id': match['gameId'], 'queue_type': match['queue']})

draft_pick = [g['game_id'] for g in games if g['queue_type'] == 400]

pid = 0
pick_number = []
usernames = []

for draft in draft_pick:
    game_request = requests.get(API_LOC + MATCH_LOOKUP + str(draft), params=payload)
    try:
        timestamp = game_request.json()['gameCreation']
    except:
        print game_request.json()
    players = game_request.json()['participantIdentities']
    all_players = [''.join(i for i in p['player']['summonerName'] if ord(i)<128) for p in players]
    for player in players:
        if player['player']['accountId'] == account_id:
            pid = player['participantId']
    if pid > 5:
        row = [timestamp]
        row.extend(all_players[5:])
        usernames.append(row)
        pick_number.append(pid - 5)
    else:
        row = [timestamp]
        row.extend(all_players[:5])
        usernames.append(row)
        pick_number.append(pid)

header = [['Time', 'Pick_1', 'Pick_2', 'Pick_3', 'Pick_4', 'Pick_5']]

header.extend(usernames)

with open('orders.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(header)

file.close()
