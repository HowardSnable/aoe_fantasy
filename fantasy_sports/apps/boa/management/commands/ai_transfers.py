from datetime import datetime, timezone, timedelta
from types import SimpleNamespace

from django.conf import settings

from django.core.management.base import BaseCommand

from fantasy_sports.apps.boa.models import *

import logging
logging.basicConfig(filename='./ai_transfers.log', encoding='utf-8', level=logging.DEBUG)


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        for league in League.objects.all():
            for player in Player.objects.all():
                offers = Offer.objects.filter(
                    league=league,
                    player=player,
                    status=Offer.STATUS_OPEN,
                    reciever=None
                    )
                offer_list = list(offers)
                offer_list.sort(reverse=True)

                if not offer_list:
                    continue

                best_offer = offer_list[0]

                # has to pay minimum price
                if best_offer.price >= best_offer.player.def_price:
                    best_offer.accept()
                    logging.info(f'Accepted: {best_offer.print()}.')
                else:
                    best_offer.decline()
                    logging.info(f'Declined: {best_offer.print()}.')

                for offer in offer_list[1:]:
                    offer.decline()
                    logging.info(f'Declined: {offer.print()}.')


