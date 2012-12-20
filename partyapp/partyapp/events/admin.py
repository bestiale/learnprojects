from django.contrib import admin
from .models import Club, Party, Guest

class ClubAdmin(admin.ModelAdmin):
	pass

class PartyAdmin(admin.ModelAdmin):
	pass

class GuestAdmin(admin.ModelAdmin):
	pass

admin.site.register(Club, ClubAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)