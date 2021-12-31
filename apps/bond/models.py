from django.db import models
from apps.users.models import CandyUser


CURRENCY = (
    ('usd', '$USD'),
    ('cad', '$CAD'),
)

BOND_STATUS = (
    ('new', 'New'),
    ('pending_desk_approval', 'Pending Desk Approval'),
    ('approved_for_sale', 'Approved For Sale'),
    ('sold', 'Sold'),
    ('on_hold', 'On Hold'),
    ('active', 'Active'),

)


class Bond(models.Model):
    bond_owner = models.ForeignKey(CandyUser, on_delete=models.CASCADE)
    bond_id = models.CharField(max_length=50, null=False, blank=False)
    isin = models.CharField(max_length=50, null=False, blank=False, unique=True)
    currency = models.CharField(max_length=20, choices=CURRENCY, blank=True, null=True)
    purchase_amount = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    amount_for_sale = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    balance_on_deposit = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    bank_issue = models.CharField(max_length=10, null=True, blank=True)
    interest_coupon = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=32, choices=BOND_STATUS, blank=True, null=True)


    class Meta:
        permissions = [
            ("can_approve_for_sale", "Can approve for sale"),
            ("can_change_status", "Can change status"),
        ]

    def __str__(self):
        return self.bond_id





