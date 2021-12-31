
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from .models import ReferralCode

class ReferralCodeListView(LoginRequiredMixin, ListView):
    template_name = 'mlm/referral_link_list.html'
    model = ReferralCode

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        qs = ReferralCode.objects.filter(created_by=self.request.user)
        return qs

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


