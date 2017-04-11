from django.core.urlresolvers import reverse_lazy
from django.db import models

from fantasy_sports.models import (
    AbstractTeam,
    #  AbstractTournament,
    AbstractPlayer,
    AbstractLeague,
)


class League(AbstractLeague):
    # number of tennis leagues a user can administrate
    MAX_LEAGUES_PER_ADMIN = 10

    max_teams_per_league = models.PositiveIntegerField()
    max_players_per_team = models.PositiveIntegerField()
    max_injured_players_per_team = models.PositiveIntegerField()

    @property
    def is_administrator_valid(self):
        admin = self.administrator
        if admin.league_set.count() < self.MAX_LEAGUES_PER_ADMIN:
            return True

        return False

    def get_absolute_url(self):
        return reverse_lazy('tennis:display_league', args=[str(self.id)])


class Team(AbstractTeam):
    league = models.ForeignKey(League)


class Player(AbstractPlayer):
    team = models.ForeignKey(Team)
    world_ranking = models.PositiveIntegerField()


class Tournament(AbstractTeam):
    SURFACE_CHOICES = (
        ('HARD', 'Hard'),
        ('GRASS', 'Grass'),
        ('CLAY', 'Clay'),
        ('OTHER', 'Other'),
    )

    TOURNAMENT_LEVEL_CHOICES = (
        ('GRAND_SLAM', 'Grand Slam'),
        ('ATP_WORLD_TOUR_FINALS', 'ATP World Tour Finals'),
        ('ATP_WORLD_TOUR_MASTERS_1000', 'ATP World Tour Masters 1000'),
        ('ATP_WORLD_TOUR_MASTERS_500', 'ATP World Tour 500 Series'),
        ('ATP_WORLD_TOUR_MASTERS_250', 'ATP World Tour 250 Series'),
        ('ATP_CHALLENGER_TOUR', 'ATP Challenger Tour'),
    )

    surface = models.CharField(
        max_length=20,
        choices=SURFACE_CHOICES,
    )
    tournament_level = models.CharField(
        max_length=50,
        choices=TOURNAMENT_LEVEL_CHOICES,
    )


class Match(models.Model):
    ROUND_CHOICES = (
        ('128', 'Round of 128'),
        ('64', 'Round of 64'),
        ('32', 'Round of 32'),
        ('16', 'Round of 16'),
        ('8', 'Quarter-Finals'),
        ('4', 'Semi-Finals'),
        ('2', 'Finals'),
    )

    player1 = models.ForeignKey(Player, related_name='player1')
    player2 = models.ForeignKey(Player, related_name='player2')
    tournament = models.ForeignKey(Tournament)
    tournament_round = models.CharField(max_length=10, choices=ROUND_CHOICES)
    winner = models.ForeignKey(Player, related_name='winner')
    score = models.CharField(max_length=100)
    date_played = models.DateField()
    number_sets = models.PositiveIntegerField()

    class Meta:
        unique_together = (('player1', 'player2', 'tournament'),)
