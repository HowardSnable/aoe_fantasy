from datetime import datetime, timezone, timedelta
from types import SimpleNamespace

from django.conf import settings

from django.core.management.base import BaseCommand

from fantasy_sports.apps.boa.models import *

import logging
logging.basicConfig(filename='./ai_transfers.log', encoding='utf-8', level=logging.DEBUG)


def generate_result(player, matchday, league):
    points = 0.
    games_pocket = games_flank = 0
    for match in Match.objects.filter(team1=player.team, matchday=matchday) | \
                 Match.objects.filter(team2=player.team, matchday=matchday):
        for game in Game.objects.filter(match=match):
            pts, pocket, flank = game.get_points(player, league)
            points += pts
            games_pocket += int(pocket)
            games_flank += int(flank)
        result = Result(points=points,
                        matchday=matchday,
                        player=player,
                        games_pocket=games_pocket,
                        games_as_flank=games_flank)
        result.save()


def award_points(lineup: LineUp, matchday: MatchDay, league: League):
    if lineup:
        points = lineup.compute_points(matchday, league)
        for match in Match.objects.filter(matchday=matchday):
            for game in Game.objects.filter(match=match):
                points += game.get_points_position(lineup, league)
        manager = lineup.manager
        manager.points += points
        manager.save()


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('day_id', nargs='+', type=int)

    def handle(self, *args, **options):
        matchday_id = int(options["day_id"].pop())
        matchday = MatchDay.objects.get(id=matchday_id)
        if matchday.is_booked:
            logging.error(f"Matchday with id {matchday_id} has already been booked!")
            return
        league = League.objects.first()

        # generate results independent of lineup and league
        for player in Player.objects.all():
            generate_result(player, matchday, league)

        # get points for positions for each manager and save
        for lineup in LineUp.objects.all():
            award_points(lineup, matchday, league)

        matchday.book()
