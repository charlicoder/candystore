from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BondModelForm
from .models import *


class BondCreateView(LoginRequiredMixin, CreateView):
    model = Bond
    # fields = '__all__'
    form_class = BondModelForm
    template_name = 'bond/bond_create_form.html'
    success_url = 'bonds/'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.status = 'new'
        form.bond_owner = self.request.user
        # import pdb; pdb.set_trace();
        form.save()
        return redirect(reverse_lazy('bond:bond_list'))


class BondListView(LoginRequiredMixin, ListView):
    template_name = 'bond/bond_list.html'
    model = Bond

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        qs = Bond.objects.filter(bond_owner=self.request.user)
        return qs




class BondRequestForSellView(LoginRequiredMixin, UpdateView):
    model = Bond
    fields = ('amount_for_sale', 'interest_coupon', 'discount_price',)
    template_name = 'bond/bond_update_form.html'
    success_url = 'bonds/'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.status = 'pending_desk_approval'
        form.save()
        return redirect(reverse_lazy('bond:pending_desk_approval'))


class BondDetailView(LoginRequiredMixin, DetailView):
    model = Bond


class BondListPendingApprovalView(LoginRequiredMixin, ListView):
    template_name = 'bond/bond_pending_desk_approval.html'
    model = Bond
    success_url = 'bond/'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(status='pending_desk_approval')

        return qs


class BondApproveForSellView(LoginRequiredMixin, UpdateView):
    model = Bond
    fields = ('status',)
    template_name = 'bond/bond_update_form.html'
    success_url = 'bonds/'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.status = 'approved_for_sale'
        form.save()
        return redirect(reverse_lazy('bond:bond_list_for_sale'))


class BondUpdateSoldView(LoginRequiredMixin, UpdateView):
    model = Bond
    fields = ('status',)
    template_name = 'bond/bond_update_form.html'
    success_url = 'bonds/'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.status = 'sold'
        form.save()
        return redirect(reverse_lazy('bond:bond_list_sold'))


class BondListApprovedForSellView(LoginRequiredMixin, ListView):
    template_name = 'bond/bond_for_sale.html'
    model = Bond
    success_url = 'bond/'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(status='approved_for_sale')

        return qs


class BondListSoldView(LoginRequiredMixin, ListView):
    template_name = 'bond/bond_list_sold.html'
    model = Bond
    success_url = 'bond/'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(status='sold')

        return qs