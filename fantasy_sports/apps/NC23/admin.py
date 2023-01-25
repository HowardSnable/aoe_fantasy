from django.contrib import admin
from .models import *

admin.site.enable_nav_sidebar = False

admin.site.register(League)
admin.site.register(Manager)
admin.site.register(Team)
admin.site.register(MatchDay)
admin.site.register(LineUp)
admin.site.register(Offer)
admin.site.register(Result)
admin.site.register(TransferMarket)
admin.site.register(Poll)
admin.site.register(Vote)

admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Game)
