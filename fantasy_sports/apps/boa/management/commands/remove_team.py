from django.utils import timezone, timezone, timedelta
from types import SimpleNamespace

from django.conf import settings

from django.core.management.base import BaseCommand

from fantasy_sports.apps.boa.models import *

import logging
logging.basicConfig(filename='./remove_teams.log', level=logging.DEBUG)


def validate_args(args):
    team = Team.objects.get(name=args['team'])
    assert team.is_alive, f"Team {team.name} already out!"
    compensation = int(args['compensation'])
    return team, compensation


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--team')
        parser.add_argument('--compensation')

    def handle(self, *args, **options):

        try:
            team, compensation = validate_args(options)
        except Exception as e:
            logging.error(e)
            print(e)
            return

        for player in Player.objects.filter(team=team):
            for manager in player.manager.all():
                manager.budget += compensation
                logging.info(f"Compensating {manager.name} with {compensation} for {team}.")
                manager.save()

        team.is_alive = False
        team.save()



