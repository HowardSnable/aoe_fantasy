import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from ..models import Manager, TransferMarket, Offer, League, Player
from ..forms import CreateOfferForm


class DisplayLeague(LoginRequiredMixin, View):
    http_method_names = [U'get', U'post']
    template_name = 'boa/display_league.html'

    def get(self, request, *args, **kwargs):
        my_league = kwargs['pk']
        manager = Manager.objects.filter(
            user=self.request.user,
            league_id=my_league,
        ).first()
        all_managers = Manager.objects.filter(
            league_id=my_league,
        )
        transfer_market = TransferMarket.objects.filter(
            league_id=my_league,
            start_date__lte=datetime.datetime.utcnow(),
            end_date__gte=datetime.datetime.utcnow(),
        )
        old_transfers = Offer.objects.filter(
            league_id=my_league,
            status=Offer.STATUS_ACCEPTED,
        )
        offers_in = Offer.objects.filter(
            league_id=my_league,
            status=Offer.STATUS_OPEN,
            reciever__user=self.request.user,
        )
        offers_out = Offer.objects.filter(
            league_id=my_league,
            status=Offer.STATUS_OPEN,
            sender__user=self.request.user,
        )
        my_players = Player.objects.filter(
            manager__user=self.request.user,
        )

        offer_form = CreateOfferForm()

        context = {
            'league': my_league,
            'manager': manager,
            'all_managers': all_managers,
            'transfer_market': transfer_market,
            'old_transfers': old_transfers,
            'offers_in': offers_in,
            'offers_out': offers_out,
            'my_players': my_players,
            'offer_form': offer_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreateOfferForm(request.POST)
        my_league = League.objects.get(id=kwargs['pk'])
        my_player = Player.objects.get(id=request.POST['player'])
        my_manager = Manager.objects.get(user=request.user, league=my_league)
        my_owner = my_player.owner.filter(league=my_league).first()
        if form.is_valid():
            offer = Offer()
            offer.player = my_player
            offer.start_date = datetime.datetime.utcnow()
            offer.end_date = request.POST['end_date']
            offer.price = request.POST['price']
            offer.sender = my_manager
            offer.status = Offer.STATUS_OPEN
            offer.reciever = my_owner
            offer.league = my_league
            offer.save()

            messages.success(
                request,
                'Successfully sent offer.'
            )
            return self.get(self, request, *args, **kwargs)
