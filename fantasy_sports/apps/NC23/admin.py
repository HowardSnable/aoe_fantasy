from django.contrib import admin
from .models import *

admin.site.enable_nav_sidebar = False

admin.site.register(League)
admin.site.register(Manager)
admin.site.register(MatchDay)
admin.site.register(LineUp)
admin.site.register(Offer)
admin.site.register(Result)
admin.site.register(TransferMarket)
admin.site.register(Poll)
admin.site.register(Vote)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['liquipedia']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['team']
    exclude = ['manager']
    search_fields = ['name']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    autocomplete_fields = ['team1', 'team2']
    search_fields = ['team1', 'team2']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    autocomplete_fields = ['w1', 'w2', 'w3', 'w4', 'l1', 'l2', 'l3', 'l4']

