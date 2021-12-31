from django import forms

from .models import *


class BondModelForm(forms.ModelForm):
    class Meta:
        model = Bond
        fields = [
            'bond_id',
            'isin',
            'currency',
            'purchase_amount',
            'amount_for_sale',
            'balance_on_deposit',
            'bank_issue',
            'interest_coupon',
            'discount_price',
            'end_date',

        ]

        widgets = {
            'bond_id': forms.TextInput(attrs={'class': 'form-control'}),
            'isin': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'purchase_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_for_sale': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance_on_deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_issue': forms.TextInput(attrs={'class': 'form-control'}),
            'interest_coupon': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),


        }