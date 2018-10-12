from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=200)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    games = models.IntegerField(default=0)
    pushups = models.IntegerField(default=0)
    pushups_done = models.IntegerField(default=0)
    accountId = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Match(models.Model):
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    #pushups = models.IntegerField(default=0)
    gameId = models.IntegerField(default=0)
    accountId = models.IntegerField(default=0)