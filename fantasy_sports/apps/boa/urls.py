from django.urls import re_path

from . import views

app_name = 'boa'

urlpatterns = [
    re_path(
        r'^home/$',
        views.Home.as_view(),
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
]
