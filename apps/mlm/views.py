
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from .models import ReferralCode, ReferralUserProfile
# from users.models import CandyUser


class ReferralCodeListView(LoginRequiredMixin, ListView):
    template_name = 'mlm/referral_link_list.html'
    model = ReferralCode

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        qs = ReferralCode.objects.filter(created_by=self.request.user)
        return qs


class ReferralCodeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mlm/referral_link_detail.html'
    model = ReferralCode
    # success_url = reverse_lazy('mlm:code_list')

    def get_object(self, queryset=None):
        # import pdb;
        # pdb.set_trace();
        pk = self.kwargs.get('pk')

        obj = ReferralCode.objects.get(pk=pk)

        return obj


class ReferralCodeBuddyListView(LoginRequiredMixin, ListView):
    template_name = 'mlm/referral_code_buddy_list.html'
    model = ReferralUserProfile

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        pk = self.kwargs.get('pk')
        code = ReferralCode.objects.get(pk=pk)
        qs = ReferralUserProfile.objects.filter(referral_code=code)
        return qs

    def get_context_data(self, object_list=None, **kwargs):
        # import pdb;
        # pdb.set_trace()
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        code = ReferralCode.objects.get(pk=pk)
        context['code'] = code.token
        # qs = ReferralUserProfile.objects.filter(referral_code=code)

        return context


class ReferralCodeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'mlm/referral_link_create.html'
    model = ReferralCode
    fields = ['commission', ]
    success_url = reverse_lazy('mlm:code_list')

    def form_valid(self, form):
        # import pdb; pdb.set_trace();
        if form.is_valid():
            code = form.save(commit=False)
            code.created_by = self.request.user
            code.status = 'new'
            code.save()
            return redirect(reverse_lazy('mlm:code_list'))
        return super().form_valid(form)


class CandyUserBuddyListView(LoginRequiredMixin, ListView):
    template_name = 'mlm/candyuser_buddy_list.html'
    model = ReferralUserProfile

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        qs = ReferralUserProfile.objects.filter(referrer=self.request.user)
        return qs


class ReferralUserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referraluser_detail.html'


class ReferralBuddyListView(LoginRequiredMixin, TemplateView):
    template_name = 'mlm/referral_buddy_list.html'


