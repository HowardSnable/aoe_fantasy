from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone

from datetime import date


from ..models import Poll, Vote, Player
from ..forms import VoteForm

N_BEST_PLAYERS = 5


def get_polls():
    dtime = timezone.now()
    if Poll.objects.filter(start__lte=dtime, end__gte=dtime).exists():
        current_poll = Poll.objects.get(start__lte=dtime, end__gte=dtime)
    else:
        current_poll = None

    previous_polls = Poll.objects.filter(end__lte=dtime)
    future_polls = Poll.objects.filter(start__gte=dtime).order_by('start')
    if future_polls:
        next_poll_start = future_polls.first().start
    else:
        next_poll_start = None
    return (current_poll,
            previous_polls,
            next_poll_start
            )


def get_vote(user, poll):
    try:
        vote = Vote.objects.get(poll=poll, user=user)
    except Vote.DoesNotExist:
        vote = None
    return vote


def get_results(polls):
    results = [(p.id, p.best_players(N_BEST_PLAYERS)) for p in polls]
    return dict(results)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class VoteView(LoginRequiredMixin, View):
    http_method_names = [u'get', U'post']
    template_name = 'nc23/vote.html'

    def get_context_data(self):
        context = {}

        user = self.request.user
        poll, old_polls, next_poll_start = get_polls()
        results = get_results(old_polls)
        context.update({
            'current_poll': poll,
            'user': user,
            'old_polls': old_polls,
            'results': results,
            'today': date.today(),
        })
        if not poll:
            context.update({'next_poll_date': next_poll_start})
            return context

        #
        form = VoteForm()
        vote = get_vote(user, poll)
        context.update({
            'form': form,
            'vote': vote,
        })

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        context = self.get_context_data()
        if request.POST.get('delete_vote_button'):
            vote = context.get('vote')
            if vote:
                vote.delete()

            messages.success(
                request,
                'Vote deleted.'
            )
            # reload context without vote
            context = self.get_context_data()
            return render(request, self.template_name, context)

        # sanity checks
        if not context["current_poll"]:
            messages.error(
                request,
                'Voting is closed.'
            )
            return render(request, self.template_name, context)

        user = context["user"]
        poll = context["current_poll"]
        ip = get_client_ip(request)

        if Vote.objects.filter(user=user, poll=poll):
            messages.warning(
                request,
                'You have voted already.'
            )
            return render(request, self.template_name, context)

        if Vote.objects.filter(ip=ip):
            messages.warning(
                request,
                'There was already a vote from your IP address.'
            )
            return render(request, self.template_name, context)

        # add vote
        voted_player = Player.objects.get(id=request.POST.get("voted_player"))
        vote = Vote(poll=poll,
                    player=voted_player,
                    user=user,
                    ip=ip)
        vote.save()

        messages.success(
            request,
            'Voting successful.'
        )
        context = self.get_context_data()
        return render(request, self.template_name, context)
