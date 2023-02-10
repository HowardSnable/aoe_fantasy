import random
from django.utils import timezone
from types import SimpleNamespace

from django.conf import settings

from django.core.management.base import BaseCommand

from fantasy_sports.apps.nc23.models import *

import logging



def add_transfers(league, old_transfers):
    num_transfers = league.transfers_per_day
    # add more players to transfer market in new leagues
    if not old_transfers:
        num_transfers *= 1 

    old_player_ids = [transfer.player.id for transfer in old_transfers]  # not necessarily DauT
    managers = Manager.objects.filter(league=league)
    new_players = list(
        Player.objects.exclude(
            id__in=old_player_ids).exclude(
            manager__in=managers).exclude(
            team__is_alive=False)
        )

    # add old players until enough or none left
    old_list = list(old_transfers)
    while len(new_players) < num_transfers:
        if not old_transfers:
            break
        new_players.append(old_list.pop().player)


    random.shuffle(new_players)
    if len(new_players) > num_transfers:
        new_players = new_players[0:num_transfers]

    for player in new_players:
        transfer = TransferMarket(player=player,
                                  league=league,
                                  manager=None,
                                  start_date=timezone.now().replace(tzinfo=timezone.utc),
                                  price=player.def_price)
        transfer.save()


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        logging.getLogger('nc23_manager')
        for league in League.objects.all():
            transfers = TransferMarket.objects.filter(league=league, manager=None)
            add_transfers(league, transfers)

            for transfer in transfers:
            #     for offer in Offer.objects.filter(league=league, player=transfer.player):
            #         offer.decline()
                transfer.delete()


