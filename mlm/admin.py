from django.contrib import admin
from .models import ReferalCode, CandyUserReferral

# Register your models here.
# class MarketingAdminArea(admin.AdminSite):
#     site_header = 'Marketing Admin Area'

# marketing_site = MarketingAdminArea(name='marketing')

# marketing_site.register(ReferalCode)

# marketing_site.register(ReferalCode)


class ReferalCodeAdmin(admin.ModelAdmin):
    list_display = ('token', 'created_by', 'status',)

admin.site.register(ReferalCode, ReferalCodeAdmin)


class CandyUserReferralAdmin(admin.ModelAdmin):
    list_display = ('parent', 'referral_code', 'child', 'status',)

admin.site.register(CandyUserReferral, CandyUserReferralAdmin)


