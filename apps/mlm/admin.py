from django.contrib import admin
from .models import ReferralCode, ReferralUserProfile

# Register your models here.
# class MarketingAdminArea(admin.AdminSite):
#     site_header = 'Marketing Admin Area'

# marketing_site = MarketingAdminArea(name='marketing')

# marketing_site.register(ReferalCode)

# marketing_site.register(ReferalCode)


class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('token', 'created_by', 'status', 'commission', 'users_count')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(ReferralCode, ReferralCodeAdmin)


class ReferralUserProfileAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referral_code', 'user', 'commission', 'status',)


admin.site.register(ReferralUserProfile, ReferralUserProfileAdmin)


