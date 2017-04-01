from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^home/$',
        views.Home.as_view(),
        name='home'
    ),
    url(
        r'^create_league/$',
        views.CreateLeague.as_view(),
        name='create_league'
    ),
    url(
        r'^find_league/$',
        views.FindLeague.as_view(),
        name='find_league'
    ),
    url(
        r'^my_leagues/$',
        views.MyLeagues.as_view(),
        name='my_leagues'
    ),
    url(
        r'^league/(?P<pk>\d+)$',
        views.DisplayLeague.as_view(),
        name='display_league'
    ),
    url(
        r'^league/(?P<pk>\d+)/update$',
        views.UpdateLeague.as_view(),
        name='update_league'
    ),
]
