from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from fantasy_sports.apps.nc23.models import *

import logging

def generate_result(player, matchday, league, top_players):
    points = 0.
    games_pocket = games_flank = 0

    if player == top_players[0]:
        points += POINTS_FOR_VOTE1
        logging.info(f'{POINTS_FOR_VOTE1} extra points for {player.name}')
    if player == top_players[1]:
        points += POINTS_FOR_VOTE2
        logging.info(f'{POINTS_FOR_VOTE2} extra points for {player.name}')
    if player == top_players[2]:
        points += POINTS_FOR_VOTE3
        logging.info(f'{POINTS_FOR_VOTE3} extra points for {player.name}')

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
                        games_flank=games_flank)
        result.save()


def award_points(lineup: LineUp, matchday: MatchDay, league: League):
    if lineup and lineup.get_players():
        points = lineup.compute_points(matchday, league)
        for match in Match.objects.filter(matchday=matchday):
            for game in Game.objects.filter(match=match):
                points += game.get_points_position(lineup, league)

        # punish empty linueps
        points += (N_PLAYERS - len(lineup.get_players())) * POINTS_FOR_EMPTY
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

        logging.basicConfig(filename=f'./points_{matchday_id}.log', level=logging.DEBUG)
        logging.info(f'Booking Matchday {matchday} with id {matchday_id} at {timezone.now()}.')

        if matchday.is_booked:
            logging.error(f"Matchday with id {matchday_id} has already been booked!")
            return
        league = League.objects.first()

        try:
            poll = Poll.objects.get(matchday=matchday)
            best_players = list(list(zip(*(poll.best_players(3))))[0])
            if len(best_players) < 3:
                best_players += [None] * (3 - len(best_players))
            # close poll
            poll.end = timezone.now()
            poll.save()
            logging.info(f'Top votes are {[plr.name for plr in best_players if plr]}. Poll is closed.')
        except ObjectDoesNotExist as error:
            best_players = [None, None, None]
            logging.warning(f'Could not find best players. Continuing anyways. {error}')


        # generate results independent of lineup and league
        for player in Player.objects.all():
            generate_result(player, matchday, league, best_players)

        logging.info(f"Results generated for all players.")

        # get points for positions for each manager and save
        for lineup in LineUp.objects.all():
            award_points(lineup, matchday, league)

        logging.info(f"Points awarded for all lineups.")

        matchday.book()
        logging.info(f"Booking completed.")

