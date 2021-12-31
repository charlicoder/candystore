from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import (
    ReferralCodeListView,
    ReferralCodeDetailView,
    ReferralCodeCreateView,
    ReferralBuddyListView,
    # ReferralUserListView,
    # ReferralUserDetailView
)

app_name = 'mlm'

urlpatterns = [
    path('test/', TemplateView.as_view(template_name='mlm/test.html'), name='test'),
    path('referral-code/', ReferralCodeListView.as_view(), name='code_list'),
    path('referral-code/<int:pk>/detail/', ReferralCodeDetailView.as_view(), name='code_details'),
    path('referral/detail/', ReferralCodeDetailView.as_view(), name='link-detail'),
    path('referral/create/', ReferralCodeCreateView.as_view(), name='create-link'),

    path('referral/buddy/list/', ReferralBuddyListView.as_view(), name='referral-buddy-list'),

]
