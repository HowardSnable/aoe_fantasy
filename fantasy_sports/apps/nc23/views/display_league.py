from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils import timezone
from ..models import Manager, TransferMarket, Offer, League, Player, LineUp, MatchDay
from ..forms import CreateOfferForm, CreateTransferForm, CreateLineUpForm
from .league_form_processing import offer_delete, offer_accept, create_transfer, delete_transfer, handle_lineup_form, \
    handle_offer_form, is_matchday
from .filters import get_item


def get_forms(context):
    transfers = TransferMarket.objects.filter(
        league=context.get('league')) \
        .exclude(manager=context.get('manager')
                 )
    ofr_players = [(tr.player.id, tr.player.name) for tr in transfers]
    offer_form = CreateOfferForm(tr_players=ofr_players)

    players = [(plr.id, plr.name) for plr in context.get('my_players')]
    transfer_form = CreateTransferForm(tr_players=players)

    players = [(None, '-----')] + players

    lineup = context.get('new_lineup')
    initial_dict = {}
    if lineup:
        initial_dict.update({
            'flank1': lineup.flank1,
            'pocket1': lineup.pocket1,
            'pocket2': lineup.pocket2,
            'flank2': lineup.flank2,
            'captain': lineup.captain,
        })
    if lineup:
        lineup_form = CreateLineUpForm(team_players=players, initial=initial_dict)
    else:
        lineup_form = CreateLineUpForm(team_players=players)

    return {
        'offer_form': offer_form,
        'transfer_form': transfer_form,
        'lineup_form': lineup_form,
    }


def get_matchdays():
    time_now = timezone.now()
    next_matchdays = MatchDay.objects.filter(start_date__gte=time_now).order_by('start_date')
    if next_matchdays:
        return is_matchday(), next_matchdays.first()
    return is_matchday(), None


def get_lineups(manager, current_matchday, next_matchday):

    if current_matchday:
        lineups = LineUp.objects.filter(manager=manager, matchday=current_matchday)
        if lineups:
            old_lineup = lineups.get()
        else:
            old_lineup = None
    else:
        old_lineup = None

    if next_matchday:
        lineups = LineUp.objects.filter(manager=manager, matchday=next_matchday)
        if lineups:
            new_lineup = lineups.get()
        else:
            new_lineup = None
    else:
        new_lineup = None

    return old_lineup, new_lineup


class DisplayLeague(LoginRequiredMixin, View):
    http_method_names = [U'get', U'post']
    template_name = 'nc23/display_league.html'

    def get_context(self, my_league_id):
        league = League.objects.get(id=my_league_id)
        manager = Manager.objects.filter(
            user=self.request.user,
            league_id=my_league_id,
        ).first()
        all_managers = Manager.objects.filter(
            league_id=my_league_id,
        ).order_by('-points')
        transfer_market = TransferMarket.objects.filter(
            league_id=my_league_id,
            # start_date__lte=timezone.now(),
            # end_date__gte=timezone.now(),
        )
        old_transfers = Offer.objects.filter(
            league_id=my_league_id,
            status=Offer.STATUS_ACCEPTED,
        ).order_by('end_date')
        offers_in = Offer.objects.filter(
            league_id=my_league_id,
            status=Offer.STATUS_OPEN,
            reciever__user=self.request.user,
        )
        offers_out = Offer.objects.filter(
            league_id=my_league_id,
            status=Offer.STATUS_OPEN,
            sender__user=self.request.user,
        )
        my_players = Player.objects.filter(
            manager__user=self.request.user,
            manager__league_id=my_league_id
        )
        teams = {
            manager.id: list(Player.objects.filter(manager=manager))
            for manager in Manager.objects.filter(league=my_league_id)
            }

        current_matchday, next_matchday = get_matchdays()
        old_lineup, new_lineup = get_lineups(manager, current_matchday, next_matchday)

        return {
            'league': league,
            'manager': manager,
            'all_managers': all_managers,
            'transfer_market': transfer_market,
            'old_transfers': old_transfers,
            'offers_in': offers_in,
            'offers_out': offers_out,
            'my_players': my_players,
            'teams': teams,
            'new_lineup': new_lineup,
            'old_lineup': old_lineup,
            'current_matchday': current_matchday,
            'next_matchday': next_matchday,
            'transfer_tab': False
        }

    def get(self, request, *args, **kwargs):
        my_league_id = kwargs['pk']

        context = self.get_context(my_league_id)
        users_in_league = [mgr.user for mgr in context.get("all_managers")]

        if request.user not in users_in_league:
            return redirect(reverse_lazy('nc23:join_league', args=[str(my_league_id)]))
        forms = get_forms(context)
        context.update(forms)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        my_league_id = kwargs['pk']
        my_league = League.objects.get(id=my_league_id)

        transfers = TransferMarket.objects.filter(league=my_league)
        tr_players = [(tr.player.id, tr.player.name) for tr in transfers]

        offer_form = CreateOfferForm(request.POST, tr_players=tr_players)
        lineup_form = CreateLineUpForm(request.POST)

        context = self.get_context(my_league_id)
        transfer_tab = False
    
        try:
            if request.POST.get("lineup_button"):
                handle_lineup_form(lineup_form, request,
                                   context.get('new_lineup'),
                                   context.get('manager'),
                                   context.get('next_matchday'))
            if request.POST.get("offer_button"):
                transfer_tab = True
                handle_offer_form(offer_form, request, my_league)
            if request.POST.get("transfer_delete"):
                transfer_tab = True
                delete_transfer(request.POST.get("transfer_to_delete"))
            if request.POST.get("add_transfer"):
                transfer_tab = True
                create_transfer(request, my_league)
            if request.POST.get("offer_accept"):
                transfer_tab = True
                offer_accept(request.POST.get("offer_to_accept"), context, request)
            if request.POST.get("offer_decline"):
                transfer_tab = True
                offer_delete(request.POST.get("offer_to_decline"))
            if request.POST.get("offer_delete"):
                transfer_tab = True
                offer_delete(request.POST.get("offer_to_delete"))
        except ObjectDoesNotExist:
            messages.error(request,
                           "Could not handle your request, you probably sent it twice.")

        context = self.get_context(my_league_id)  # reload
        forms = get_forms(context)
        context.update(forms)
        context.update({'transfer_tab': transfer_tab})

        return render(request, self.template_name, context)

