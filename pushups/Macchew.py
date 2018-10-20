import json
import requests
import time
import os
from LOL_CTS.settings import BASE_DIR

end_time = int(time.time()*1000)
start_time = end_time - 259200000
api_file = open(os.path.join(BASE_DIR, "Lol_CTS\\api_key.txt"), "r")

api_key = api_file.read()
api_headers = {"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
               "X-Riot-Token": api_key,
               "Accept-Language": "en-US,en;q=0.5",
               }

class MyPlayer:
    matches = []

    def __init__(self, name):
        self.name = name
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.games = 0
        self.pushups_owed = 0
        self.pushups_done = 0
        self.resp = requests.get(
            "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+name, headers=api_headers)
        #print(self.resp.status_code)
        self.accountId = self.resp.json()["accountId"]
        self.match_account_resp = requests.get("https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(
            self.accountId)+"?endTime="+str(end_time)+"&beginTime="+str(start_time)+"&season=11", headers=api_headers)
        #print(self.match_account_resp.status_code)
        self.gameIds = []
        for game in self.match_account_resp.json()["matches"]:
            self.gameIds.append(game["gameId"])
        #print(self.name)
        #print(self.gameIds)

    def NewMatch(self, x):
        self.kills += x.getKills()
        self.deaths += x.getDeaths()
        self.assists += x.getAssists()
        self.pushups_owed += x.getDeaths() * 10
        if(x.status):
            self.games += 1
    
    def show(self):
        result = self.name + ": K:" + str(self.kills) + " D:" + str(self.deaths)
        return result

class MyMatch:

    def __init__(self, game, name, accountId):
        if(game == None):
            self.kills = 0
            self.deaths = 0
            self.assists = 0
            self.gameId = 0
            self.status = False
        else:
            self.status = True
            self.gameId = game["gameId"]
            self.accountId = accountId
            i = 0
            while name != game["participantIdentities"][i]["player"]["summonerName"]:
                if name != game["participantIdentities"][i]["player"]["summonerName"]:
                    #print(name + " is not the same as " + game["participantIdentities"][i]["player"]["summonerName"])
                    i += 1

            #print("Found " + str(game["participantIdentities"]
            #     [i]["player"]["summonerName"]))
            participant_stats = game["participants"][i]["stats"]
            #print("Kills:"+str(participant_stats["kills"]))
            self.kills = participant_stats["kills"]
            self.deaths = participant_stats["deaths"]
            self.assists = participant_stats["assists"]
            

    def getKills(self):
        return self.kills

    def getDeaths(self):
        return self.deaths

    def getAssists(self):
        return self.assists
