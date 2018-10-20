from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=200)
    #kills = models.IntegerField(default=0)
    #deaths = models.IntegerField(default=0)
    #assist = models.IntegerField(default=0)
    #games = models.IntegerField(default=0)
    #pushups = models.IntegerField(default=0)
    pushups_done = models.IntegerField(default=0)
    accountId = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    @property
    def GetDeaths(self):
        totalDeaths = 0
        match_list = Match.objects.values_list('deaths', flat=True).filter(accountId = self.accountId)
        for x in match_list:
            totalDeaths = totalDeaths + int(x)
        return totalDeaths
    
    @property
    def GetKills(self):
        totalKills = 0
        match_list = Match.objects.values_list(
            'kills', flat=True).filter(accountId=self.accountId)
        for x in match_list:
            totalKills = totalKills + int(x)
        return totalKills
    
    @property
    def GetPushups(self):
        totalPushups = 0
        match_list = Match.objects.values_list(
            'deaths', flat=True).filter(accountId=self.accountId)
        for x in match_list:
            totalPushups = totalPushups + int(x)
        totalPushups = totalPushups * 10
        return totalPushups


class Match(models.Model):
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    #pushups = models.IntegerField(default=0)
    gameId = models.IntegerField(default=0)
    accountId = models.IntegerField(default=0)
    date = models.DateField(default="2018-10-01")

    def __str__(self):
        return str(self.gameId) + ":" + str(self.accountId) \
        + "\nDeaths:" + str(self.deaths) \
        + "\nKills :" + str(self.kills)
