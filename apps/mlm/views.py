
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ReferralCodeListView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referral_link_list.html'

class ReferralCodeDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referral_link_detail.html'


class ReferralCodeCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referral_link_create.html'

    
class ReferralUserListView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referraluser_list.html'

class ReferralUserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referraluser_detail.html'


class ReferralBuddyListView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referral_buddy_list.html'


