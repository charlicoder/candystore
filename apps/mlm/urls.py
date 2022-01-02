from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import (
    ReferralCodeListView,
    ReferralCodeDetailView,
    ReferralCodeBuddyListView,
    ReferralCodeCreateView,
    CandyUserBuddyListView,
    # ReferralUserListView,
    # ReferralUserDetailView
)

app_name = 'mlm'

urlpatterns = [
    path('test/', TemplateView.as_view(template_name='mlm/test.html'), name='test'),
    path('referral-code/', ReferralCodeListView.as_view(), name='code_list'),
    path('referral-code/<int:pk>/detail/', ReferralCodeDetailView.as_view(), name='code_details'),
    path('referral-code/<int:pk>/buddy/list/', ReferralCodeBuddyListView.as_view(), name='code-buddy-list'),
    path('referral-code/create/', ReferralCodeCreateView.as_view(), name='create-code'),

    path('buddy/list/', CandyUserBuddyListView.as_view(), name='buddy-list'),

]
