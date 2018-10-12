from django.shortcuts import HttpResponse, render
from pushups.Macchew import MyPlayer, MyMatch
from .models import Player, Match
import requests, logging, time
from django.template import loader
import os
from LOL_CTS.settings import BASE_DIR

api_file = open(os.path.join(BASE_DIR, "Lol_CTS\\api_key.txt"), "r")

api_key = api_file.read()
api_headers = {"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
               "X-Riot-Token": api_key,
               "Accept-Language": "en-US,en;q=0.5",
               }
master_match = {}
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return HttpResponse("Hello, World! Be prepared for idiocy!")

def test(request):
    player_list = Player.objects.all()
    context = {'player_list': player_list}
    return render(request, 'pushups/test.html', context)

def initialize(request):
    player1 = MyPlayer("Whyki")
    player2 = MyPlayer("Macchew")
    player3 = MyPlayer("Ruffeck")
    player4 = MyPlayer("Pressed Sak")
    player5 = MyPlayer("thesteve034")

    matches1 = getMatches(player1.gameIds) 
    matches2 = getMatches(player2.gameIds)
    matches3 = getMatches(player3.gameIds)
    matches4 = getMatches(player4.gameIds)
    matches5 = getMatches(player5.gameIds)

    addMatches(player1, matches1)
    addMatches(player2, matches2)
    addMatches(player3, matches3)
    addMatches(player4, matches4)
    addMatches(player5, matches5)

    for match in master_match:
       all_matches = Match.objects.values_list('gameId', flat=True).distinct()
       m = Match(gameId = match)
       m.save()
    
    return HttpResponse(player1.show() + '\n' + player2.show() + '\n' + player3.show() + '\n' + player4.show() + '\n' + player5.show())


def getMatches(x):
    match_list = []
    count = 0
    for game_id in x:
        if count == 5:
            time.sleep(1)
            count = 0
        #print(game_id)
        count += 1
        match_data = getMatchData(game_id)
        #print(match_data)
        match_list.append(match_data)
    return match_list


def getMatchData(gameId):
    count_of_players = 0

    if not gameId in master_match:
        match_url = "https://na1.api.riotgames.com/lol/match/v3/matches/"
        match_resp = requests.get(match_url + str(gameId), headers=api_headers)
        for participant in match_resp.json()["participantIdentities"]:
            #print(participant)
            if participant["player"]["summonerName"] in ["Whyki", "Pressed Sak", "Ruffeck", "Macchew", "thesteve034"]:
                count_of_players += 1

        if (count_of_players > 2):
            print(str(match_resp.json()["gameId"]))
            master_match[str(gameId)] = match_resp.json()["gameId"]
            #print("Players in Match : "+str(count_of_players))
            #print("Match Id : " + str(gameId))
        else:
            return None

        if(match_resp.status_code == 200):
            #print("Match Found")
            return match_resp.json()
        else:
            return None
    else:
        return master_match[gameId]


def addMatches(player_x, matches_x):
    for match in matches_x:
        match_y = MyMatch(match, player_x.name, player_x.accountId)
        player_x.NewMatch(match_y)
        m = Match(gameId = match_y.gameId, accountId = player_x.accountId, kills = match_y.gameId, deaths = match_y.deaths, assists = match_y.assists)
        try:
            p = Player.objects.get(name = player_x.name)
            p.kills = p.kills + match_y.kills
            p.deaths = p.deaths + match_y.deaths
            p.assist = p.assist + match_y.assists
            p.pushups = p.deaths * 10
            p.save()
        except Player.DoesNotExist:
            p = Player(name = player_x.name, kills = match_y.kills, deaths = match_y.deaths, assist = match_y.assists, accountId = player_x.accountId)
            p.save()



