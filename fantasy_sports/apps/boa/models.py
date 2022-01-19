from .constants import *

from django.urls import reverse_lazy
from django.db import models
from django.conf import settings

from fantasy_sports.models import (
    AbstractManager,
    #  AbstractTournament,
    AbstractPlayer,
    AbstractLeague,
)


class League(AbstractLeague):

    max_teams_per_league = models.PositiveIntegerField()
    max_players_per_team = models.PositiveIntegerField(default=MAX_PLAYERS_PER_TEAM)
    points_per_match_win = models.FloatField(default=POINTS_PER_MATCH_WIN)
    points_per_match_loss = models.FloatField(default=POINTS_PER_MATCH_LOSS)
    point_for_mvp = models.FloatField(default=POINT_FOR_MVP)
    captain_factor = models.FloatField(default=CAPTAIN_FACTOR)

    @property
    def is_administrator_valid(self):
        admin = self.administrator
        if admin.league_set.count() < MAX_LEAGUES_PER_ADMIN:
            return True

        return False

    def get_absolute_url(self):
        return reverse_lazy('boa:display_league', args=[str(self.id)])


class Manager(AbstractManager):
    points = models.FloatField(default=0)
    budget = models.FloatField(default=0)
    icon = models.TextField(default='')
    name = models.TextField(default='')

    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(models.Model):
    liquipedia = models.TextField(default='', blank=True)
    name = models.TextField(default='', blank=True)
    icon = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name


class Player(AbstractPlayer):
    manager = models.ManyToManyField(Manager, blank=True)
    liquipedia = models.TextField(default='', blank=True)
    aoe2net = models.TextField(default='', blank=True)
    def_price = models.FloatField(default=0)
    icon = models.TextField(default='', blank=True)
    image = models.TextField(default='', blank=True)

    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE)

    def get_price(self):
        return self.def_price

    def __str__(self):
        return self.name


class MatchDay(models.Model):
    ROUND_CHOICES = (
        ('128', 'Round of 128'),
        ('64', 'Round of 64'),
        ('32', 'Round of 32'),
        ('16', 'Round of 16'),
        ('8', 'Quarter-Finals'),
        ('4', 'Semi-Finals'),
        ('2', 'Finals'),
    )
    tournament_round = models.CharField(max_length=10, choices=ROUND_CHOICES)
    name = models.TextField(default='')
    is_active = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)

    def book(self):
        return 0 #todo implement


class Match(models.Model):
    # two teams facing each other

    score = models.TextField()
    date_played = models.DateTimeField(default=None, null=True)
    number_games = models.PositiveIntegerField(default=1)
    liquipedia = models.TextField(default='')
    winner = models.IntegerField(default=0)  # 0: not yet played, 1: team1, 2: team2

    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)
    match_day = models.ForeignKey(MatchDay, related_name='match_day', on_delete=models.CASCADE)


    def get_points(self, player: Player, as_pocket: bool):
        return 1 #todo implement

    class Meta:
        unique_together = (('team1', 'team2'),)


class Game(models.Model):
    # A single 3v3 game

    match = models.ForeignKey(Match, related_name='match', on_delete=models.CASCADE)

    w1 = models.ForeignKey(Player, related_name='w1', on_delete=models.CASCADE)
    #pocket
    w2 = models.ForeignKey(Player, related_name='w2', on_delete=models.CASCADE)
    w3 = models.ForeignKey(Player, related_name='w3', on_delete=models.CASCADE)

    l1 = models.ForeignKey(Player, related_name='l1', on_delete=models.CASCADE)
    # pocket
    l2 = models.ForeignKey(Player, related_name='l2', on_delete=models.CASCADE)
    l3 = models.ForeignKey(Player, related_name='l3', on_delete=models.CASCADE)

    mvp1 = models.ForeignKey(Player, related_name='mvp1', on_delete=models.CASCADE)
    mvp2 = models.ForeignKey(Player, related_name='mvp2', on_delete=models.CASCADE)

    def get_winners(self):
        return [self.w1, self.w2, self.w3]

    def get_losers(self):
        return [self.l1, self.l2, self.l3]

    def get_mvps(self):
        return [self.mvp1, self.mvp2]

    def get_pockets(self):
        return [self.w2, self.l2]


class LineUp(models.Model):
    FLANK1 = 1
    POCKET = 2
    FLANK2 = 3
    captain = models.IntegerField(default=POCKET)

    flank1 = models.ForeignKey(Player, related_name='flank1', on_delete=models.CASCADE)
    pocket = models.ForeignKey(Player, related_name='pocket', on_delete=models.CASCADE)
    flank2 = models.ForeignKey(Player, related_name='flank2', on_delete=models.CASCADE)
    match_day = models.ForeignKey(Player, related_name='match_day', on_delete=models.CASCADE)



    def compute_points(self):
        return 0 # todo implement


class Offer(models.Model):

    STATUS_OPEN = 0
    STATUS_ACCEPTED = 1
    STATUS_DECLINED = 2

    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)
    price = models.FloatField(default=0)
    status = models.IntegerField(default=STATUS_OPEN)
    player = models.ForeignKey(Player, related_name='player', on_delete=models.CASCADE)
    sender = models.ForeignKey(Manager, related_name='sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey(Manager, related_name='reciever', on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def accept(self):
        return 0 # todo implement

    def decline(self):
        return 0 # todo implement


class LineUpAdapter(models.Model):
    manager = models.ForeignKey(Player, related_name='owner', on_delete=models.CASCADE)
    current_line_up = models.ForeignKey(LineUp, related_name='current_line_up', on_delete=models.CASCADE)
    locked_line_up = models.ForeignKey(LineUp, related_name='locked_line_up', on_delete=models.CASCADE)


class TransferMarket(models.Model):
    player = models.ForeignKey(Player, related_name='tr_player', on_delete=models.CASCADE)
    league = models.ForeignKey(League, related_name='tr_league', on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)
