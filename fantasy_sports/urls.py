from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^accounts/',
        include('fantasy_sports.apps.account_management.urls',
                namespace='account_management')
    ),
    url(
        r'^tennis/',
        include('fantasy_sports.apps.tennis.urls',
                namespace='tennis')
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
