from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(
        'admin/',
        admin.site.urls
    ),
    re_path(
        r'^accounts/',
        include(
            'fantasy_sports.apps.account_management.urls',
            namespace='account_management'
        )
    ),
    re_path(
        r'^boa/',
        include(
            'fantasy_sports.apps.boa.urls',
            namespace='boa'
        )
    ),
    re_path(
        r'^nc23/',
        include(
            'fantasy_sports.apps.nc23.urls',
            namespace='nc23'
        )
    ),
    re_path(
        r'',
        views.redirect_view
    ),
]


