from django.contrib import admin

from .models import *


class BondAdmin(admin.ModelAdmin):
    list_display = ('bond_id', 'status',)


admin.site.register(Bond, BondAdmin)