import datetime
import logging

from .constants import *

from django.urls import reverse_lazy
from django.db import models
from django.conf import settings


from django.utils.safestring import mark_safe
from fantasy_sports.models import (
    AbstractManager,
    #  AbstractTournament,
    AbstractPlayer,
    AbstractLeague,
)


class League(AbstractLeague):

    max_teams_per_league = models.PositiveIntegerField(default=10)
    max_players_per_team = models.PositiveIntegerField(default=MAX_PLAYERS_PER_TEAM)
    points_per_match_win = models.FloatField(default=POINTS_PER_MATCH_WIN)
    points_per_match_loss = models.FloatField(default=POINTS_PER_MATCH_LOSS)
    point_for_mvp = models.FloatField(default=POINT_FOR_MVP)
    captain_factor = models.FloatField(default=CAPTAIN_FACTOR)
    points_for_position = models.FloatField(default=POINTS_FOR_POSITION)
    transfers_per_day = models.IntegerField(default=TRANSFERS_PER_DAY)
    password = models.CharField(max_length=50, blank=True)
    @property
    def is_administrator_valid(self):
        admin = self.administrator
        if admin.league_set.count() < MAX_LEAGUES_PER_ADMIN:
            return True

        return False

    def get_absolute_url(self):
        return reverse_lazy('boa:display_league', args=[str(self.id)])

    def get_mgr_count(self):
        return Manager.objects.filter(league=self).count()

    def is_full(self):
        return self.get_mgr_count() >= self.max_teams_per_league


class Manager(AbstractManager):
    points = models.FloatField(default=0)
    budget = models.IntegerField(default=START_BUDGET)
    icon = models.TextField(default='', blank=True)
    name = models.CharField(default='Team', max_length=20)

    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(models.Model):
    liquipedia = models.TextField(default='', blank=True)
    name = models.TextField(default='', blank=True)
    long_name = models.TextField(default='', blank=True)
    icon = models.TextField(default='', blank=True)
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def linked_name(self):
        return mark_safe(f"""<a href="{self.liquipedia}">
                          <img src="{ f'{settings.STATIC_URL}icons/teams/{self.icon}' }"
                          height="18"
                          title="{self.long_name}">
                          </a>""")

    def long_linked_name(self):
        return mark_safe(f'<a href="{self.liquipedia}">{self.long_name}</a>')

    def get_top_worth(self, t_start, t_end, max_p: int):
        values = [plr.networth(t_start, t_end)[0] for plr in Player.objects.filter(team=self)]
        values.sort(reverse=True)
        return sum(values[:max_p])


class Player(AbstractPlayer):
    manager = models.ManyToManyField(Manager, blank=True)
    liquipedia = models.TextField(default='', blank=True)
    aoe2net = models.TextField(default='', blank=True)
    def_price = models.IntegerField(default=0)
    icon = models.TextField(default='', blank=True)
    image = models.TextField(default='', blank=True)

    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE)

    def get_price(self):
        return self.def_price

    def get_points(self, matchday=None):
        if matchday:
            matchdays = [matchday]
        else:
            matchdays = MatchDay.objects.all()
        results = Result.objects.filter(player=self,
                                        matchday__in=matchdays)
        points = 0.
        for result in results:
            points += result.points
        return points

    def get_manager(self, league):
        managers = [mgr for mgr in self.manager.all() if mgr.league == league]
        if managers:
            return managers[0]
        else:
            return None

    def linked_name(self):
        return mark_safe(f'<a href="{self.liquipedia}">{self.name}</a>')

    def compact_linked(self):
        return mark_safe(f' {self.team.linked_name()}{self.linked_name()}')

    def table_name(self):
        return mark_safe(f' <td>{self.team.linked_name()}</td><td">{self.linked_name()}</td>')

    def networth(self, t_start, t_end):
        transfers = Offer.objects.filter(status=Offer.STATUS_ACCEPTED,
                                         player=self,
                                         end_date__gte=t_start,
                                         end_date__lte=t_end)
        if transfers:
            return sum([ofr.price for ofr in transfers]) / transfers.count(), transfers.count()
        else:
            return self.def_price, 0

    def __str__(self):
        return self.name


class MatchDay(models.Model):
    ROUND_CHOICES = (
       # ('128', 'Round of 128'),
       # ('64', 'Round of 64'),
        ('G1', 'Group stage round 1'),
        ('G2', 'Group stage round 2'),
        ('G3', 'Group stage round 3'),
        ('16', 'Round of 16'),
        ('8', 'Quarter-Finals'),
        ('4', 'Semi-Finals'),
        ('2', 'Finals'),
    )
    tournament_round = models.CharField(max_length=10, choices=ROUND_CHOICES)
    is_active = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.tournament_round

    def book(self):
        self.is_booked = True
        self.save()


class Match(models.Model):
    # two teams facing each other

    score = models.TextField(null=True, blank=True)
    date_played = models.DateTimeField(default=None, null=True)
    number_games = models.PositiveIntegerField(default=1)
    winner = models.IntegerField(default=0, null=True)  # 0: not yet played, 1: team1, 2: team2

    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)
    matchday = models.ForeignKey(MatchDay, related_name='match_day', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.team1} vs {self.team2}, {self.matchday}"

    class Meta:
        unique_together = (('team1', 'team2'),)


class LineUp(models.Model):
    NONE = 0
    FLANK1 = 1
    POCKET = 2
    FLANK2 = 3
    captain = models.IntegerField(default=NONE)

    flank1 = models.ForeignKey(Player, related_name='flank1', on_delete=models.CASCADE, null=True, blank=True)
    pocket = models.ForeignKey(Player, related_name='pocket', on_delete=models.CASCADE, null=True, blank=True)
    flank2 = models.ForeignKey(Player, related_name='flank2', on_delete=models.CASCADE, null=True, blank=True)
    matchday = models.ForeignKey(MatchDay, related_name='l_match_day', on_delete=models.CASCADE, null=True)
    manager = models.OneToOneField(Manager, related_name='lineup_manager', on_delete=models.CASCADE, primary_key=True)

    def compute_points(self,  matchday: MatchDay, league: League):
        results = Result.objects.filter(player__in=self.get_players(), matchday=matchday)
        points = 0.
        for result in results:
            points += result.points

        if self.get_captain():
            captain_results = Result.objects.filter(player=self.get_captain(), matchday=matchday)
            for res in captain_results:
                points += res.points * (league.captain_factor - 1)
        return points

    def get_players(self):
        players = [self.flank1, self.pocket, self.flank2]
        return list(filter(None, players))

    def get_captain(self):
        if not self.captain:
            return None
        if self.captain == self.FLANK1:
            return self.flank1
        if self.captain == self.POCKET:
            return self.pocket
        if self.captain == self.FLANK2:
            return self.flank2


class Game(models.Model):
    # A single 3v3 game

    match = models.ForeignKey(Match, related_name='match',
                              on_delete=models.CASCADE)

    w1 = models.ForeignKey(Player, related_name='w1',
                           on_delete=models.CASCADE,
                           )
    #pocket
    w2 = models.ForeignKey(Player, related_name='w2',
                           on_delete=models.CASCADE,
                           )
    w3 = models.ForeignKey(Player,
                           related_name='w3',
                           on_delete=models.CASCADE,
                           )

    l1 = models.ForeignKey(Player,
                           related_name='l1',
                           on_delete=models.CASCADE,
                           )
    # pocket
    l2 = models.ForeignKey(Player,
                           related_name='l2',
                           on_delete=models.CASCADE,
                           )
    l3 = models.ForeignKey(Player,
                           related_name='l3',
                           on_delete=models.CASCADE,
                           )

    mvp1 = models.ForeignKey(Player,
                             related_name='mvp1',
                             on_delete=models.CASCADE,
                             )
    mvp2 = models.ForeignKey(Player,
                             related_name='mvp2',
                             on_delete=models.CASCADE,
                             )

    def get_winners(self):
        return [self.w1, self.w2, self.w3]

    def get_losers(self):
        return [self.l1, self.l2, self.l3]

    def get_mvps(self):
        return [self.mvp1, self.mvp2]

    def get_pockets(self):
        return [self.w2, self.l2]

    def get_flanks(self):
        return [self.w1, self.w3, self.l1, self.l3]

    def get_points(self, player: Player, league: League):
        points = 0.
        if player in self.get_winners():
            points += league.points_per_match_win
        if player in self.get_losers():
            points += league.points_per_match_loss
        if player in self.get_mvps():
            points += league.point_for_mvp
        return points, player in self.get_pockets(), player in self.get_flanks()

    def get_points_position(self, lineup: LineUp, league: League):
        points = 0.
        extra_captain_points = league.points_for_position * (league.captain_factor - 1.)
        if lineup.flank1 in self.get_flanks():
            points += league.points_for_position
            if lineup.captain == LineUp.FLANK1:
                points += extra_captain_points
        if lineup.pocket in self.get_pockets():
            points += league.points_for_position
            if lineup.captain == LineUp.POCKET:
                points += extra_captain_points
        if lineup.flank2 in self.get_flanks():
            points += league.points_for_position
            if lineup.captain == LineUp.FLANK2:
                points += extra_captain_points
        return points


class Offer(models.Model):

    STATUS_OPEN = 0
    STATUS_ACCEPTED = 1
    STATUS_DECLINED = 2

    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)
    price = models.IntegerField(default=0)
    status = models.IntegerField(default=STATUS_OPEN)
    player = models.ForeignKey(Player, related_name='player', on_delete=models.CASCADE)
    sender = models.ForeignKey(Manager, related_name='sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey(Manager, related_name='reciever', on_delete=models.CASCADE, null=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def accept(self):
        if self.status == self.STATUS_ACCEPTED:
            return
        if self.reciever:
            self.reciever.budget = self.reciever.budget + self.price
            self.reciever.save()
            self.player.manager.remove(self.reciever)
        self.player.manager.add(self.sender)
        self.player.save()
        self.end_date = datetime.datetime.utcnow()
        self.status = self.STATUS_ACCEPTED
        self.save()
        self.remove_tansfer_market()

    def decline(self):
        self.sender.budget = self.sender.budget + self.price
        self.sender.save()
        self.delete()

    def remove_tansfer_market(self):
        try:
            transfer_market = TransferMarket.objects.get(player=self.player, league=self.league)
            if transfer_market:
                transfer_market.delete()
        except TransferMarket.DoesNotExist:
            logging.warning(f'TransferMarket not found when moving {self.player} in {self.league}.')

    def __lt__(self, other):
        if self.price == other.price:
            return self.start_date > other.start_date
        return self.price < other.price

    def print(self):
        return f'Offer of {self.price} for {self.player} from {self.sender} to {self.reciever} in league {self.league}'


class TransferMarket(models.Model):
    player = models.ForeignKey(Player, related_name='tr_player', on_delete=models.CASCADE)
    league = models.ForeignKey(League, related_name='tr_league', on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, related_name='tr_manager', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)
    price = models.IntegerField(default=0)


class Result(models.Model):
    player = models.ForeignKey(Player, related_name='res_player', on_delete=models.CASCADE)
    matchday = models.ForeignKey(MatchDay, related_name='res_day', on_delete=models.CASCADE)
    points = models.FloatField()
    games_pocket = models.IntegerField(default=0)
    games_flank = models.IntegerField(default=0)
