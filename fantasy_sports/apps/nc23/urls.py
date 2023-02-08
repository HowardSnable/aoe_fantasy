from django.urls import re_path

from . import views

app_name = 'nc23'

urlpatterns = [
    re_path(
        r'^home/$',
        views.home_view,
        name='home'
    ),
    re_path(
        r'^create_league/$',
        views.CreateLeague.as_view(),
        name='create_league'
    ),
    re_path(
        r'^find_league/$',
        views.FindLeague.as_view(),
        name='find_league'
    ),
    re_path(
        r'^league/(?P<pk>\d+)/join$',
        views.JoinLeague.as_view(),
        name='join_league'
    ),
    re_path(
        r'^my_leagues/$',
        views.MyLeagues.as_view(),
        name='my_leagues'
    ),
    re_path(
        r'^league/(?P<pk>\d+)$',
        views.DisplayLeague.as_view(),
        name='display_league'
    ),
    re_path(
        r'^league/(?P<pk>\d+)/update$',
        views.UpdateLeague.as_view(),
        name='update_league'
    ),
    re_path(
        r'^results$',
        views.ResultView.as_view(),
        name='results'
    ),
    re_path(
        r'^market_info$',
        views.MarketInfoView.as_view(),
        name='market_info'
    ),
    re_path(
        r'^rules$',
        views.RulesView.as_view(),
        name='rules'
    ),
    re_path(
        r'^vote',
        views.VoteView.as_view(),
        name='vote'
    ),

    re_path(
        r'^welcome',
        views.WelcomeView.as_view(),
        name='welcome'
    ),
]
