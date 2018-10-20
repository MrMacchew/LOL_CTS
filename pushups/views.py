from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from pushups.Macchew import MyPlayer, MyMatch
from .models import Player, Match
from .forms import LoginForm
import requests, logging, time
from django.template import loader
import os
from LOL_CTS.settings import BASE_DIR
from django.contrib.auth import authenticate, login, logout


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
    player_list = Player.objects.all()
    context = { 'player_list': player_list }
    return render(request, 'index.html', context)

def summoner(request):
    player_list = Player.objects.all()
    context = {'player_list': player_list}
    return render(request, 'summoner.html', context)

def match_list(request, id):
    match_list = Match.objects.all().filter(accountId = id)

def login_view(request):
    if request.method == 'POST':
        print("POST Method")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("valid form")
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                print("user is not none")
                if user.is_active:
                    print("user is active")
                    login(request, user)
                    print(user.username + "Has Logged In")
                    return HttpResponseRedirect('/pushups')
                else:
                    print("The account has been deactivated")
            else:
                print("The username and password are incorrect")
                return render(request, 'login.html', {'form': form})
    else: 
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pushups')

def initialize(request):
    player1 = update("Whyki")
    player2 = update("Macchew")
    player3 = update("Ruffeck")
    player4 = update("Pressed Sak")
    player5 = update("thesteve034")
    
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
        print("Searching for "+ str(gameId))
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
        if not Match.objects.all().filter(gameId = match_y.gameId, accountId = player_x.accountId):
            m = Match(gameId = match_y.gameId, accountId = player_x.accountId, kills = match_y.kills, deaths = match_y.deaths, assists = match_y.assists)
            m.save()
        try:
            p = Player.objects.get(name = player_x.name)
            #p.kills = p.kills + match_y.kills
            #p.deaths = p.deaths + match_y.deaths
            #p.assist = p.assist + match_y.assists
            #p.pushups = p.deaths * 10
            p.save()
        except Player.DoesNotExist:
            p = Player(name = player_x.name,  accountId = player_x.accountId)
            p.save()

def update(name):
    player = MyPlayer(name)
    matches = getMatches(player.gameIds) 
    addMatches(player, matches)
    return player




