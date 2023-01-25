from django.utils import timezone
from django.contrib import messages
from ..models import Manager, TransferMarket, Offer, MatchDay, Player, LineUp
from .filters import get_item


def is_matchday():
    time_now = timezone.now()
    if any(MatchDay.objects.filter(start_date__lte=time_now,
                                   end_date__gte=time_now)):
        return True
    else:
        return False


def offer_delete(pk_offer):
    offer = Offer.objects.get(pk=pk_offer)
    offer.decline()


def offer_accept(pk_offer):
    offer = Offer.objects.get(pk=pk_offer)
    offer.accept()


def create_transfer(request, league):
    player_id = request.POST['player']
    player = Player.objects.get(pk=player_id)
    manager = player.get_manager(league)

    transfer_markets = TransferMarket.objects.filter(manager=manager, player=player)
    if transfer_markets:
        transfer_market = transfer_markets[0]
    else:
        transfer_market = TransferMarket()
        transfer_market.player = player
        transfer_market.league = league
        transfer_market.manager = manager
    transfer_market.price = request.POST['price']
    transfer_market.save()


def delete_transfer(pk_transfer):
    transfer = TransferMarket.objects.get(pk=pk_transfer)
    transfer.delete()


def handle_offer_form(offer_form, request, my_league):

    my_manager = Manager.objects.get(user=request.user, league=my_league)
    my_player = Player.objects.get(id=request.POST['player'])
    my_owner = my_player.manager.filter(league=my_league).first()

    if offer_form.is_valid():

        # if price higher than budget, error
        if int(request.POST['price']) > my_manager.budget:
            messages.warning(
                request,
                f'You cannot afford this offer, your budget is {my_manager.budget}'
            )
            return

        # if offer for player exists, update
        offer_old = Offer.objects.filter(
            league_id=my_league,
            status=Offer.STATUS_OPEN,
            sender__user=request.user,
            player=my_player,
        ).first()
        if offer_old:
            offer = offer_old
            my_manager.budget = my_manager.budget + int(offer_old.price)
        else:
            offer = Offer()

        offer.player = my_player
        offer.start_date = timezone.now()
        offer.end_date = timezone.now() + datetime.timedelta(days=7)
        offer.price = request.POST['price']
        offer.sender = my_manager
        offer.status = Offer.STATUS_OPEN
        offer.reciever = my_owner
        offer.league = my_league

        my_manager.budget = my_manager.budget - int(offer.price)
        my_manager.save()

        offer.save()

        messages.success(
            request,
            'Successfully sent offer.'
        )


def handle_lineup_form(lineup_form, request, my_league, lineup):

    if is_matchday():
        messages.error(request,
                       'Cannot change Line-Up while games are played!')
        return

    if lineup_form.is_valid():
        flank1 = request.POST.get('flank1')
        pocket = request.POST.get('pocket')
        flank2 = request.POST.get('flank2')
        players = [flank1, pocket, flank2]
        players = list(filter(None, players))

        if len(players) < 3:
            messages.warning(
                request,
                f'Leaving positions empty will give negative score!'
            )

        if not lineup:
            lineup = LineUp()
        if flank1:
            lineup.flank1 = Player.objects.get(id=flank1)
        else:
            lineup.flank1 = None
        if pocket:
            lineup.pocket = Player.objects.get(id=pocket)
        else:
            lineup.pocket = None
        if flank2:
            lineup.flank2 = Player.objects.get(id=flank2)
        else:
            lineup.flank2 = None
        lineup.manager = Player.objects.get(id=players[0]).get_manager(my_league)

        lineup.captain = request.POST.get('captain')
        if lineup.captain is None:
            lineup.captain = LineUp.NONE
        lineup.save()

        messages.success(
            request,
            'Successfully fielded players.'
        )
    else:
        messages.error(
            request,
            lineup_form.non_field_errors()
        )