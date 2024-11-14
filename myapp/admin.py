from django.contrib import admin

from myapp.models import Casillero

@admin.register(Casillero)
class CasilleroAdmin(admin.ModelAdmin):
    list_display = ('email', 'password')
