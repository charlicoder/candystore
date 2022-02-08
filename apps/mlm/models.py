from django.db import models
from apps.users.models import CandyUser
import secrets

REFERRAL_STATUS = (('active', 'Active'), ('inactive', 'Inactive'), ('new', 'New'))


# Create your models here.
class ReferralCode(models.Model):
    created_by = models.ForeignKey(CandyUser, on_delete=models.CASCADE, editable=False)
    token = models.CharField(max_length=100, blank=False, null=False, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    commission = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=REFERRAL_STATUS, default='new')
    users_count = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if self.id is None:
            token = secrets.token_urlsafe(32)
            self.token = token

        super().save(*args, **kwargs)
        

class ReferralUserProfile(models.Model):
    referrer = models.ForeignKey(CandyUser, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='parent')
    referral_code = models.ForeignKey(ReferralCode, on_delete=models.CASCADE, blank=False, null=False)
    user = models.OneToOneField(CandyUser, on_delete=models.CASCADE, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    commission = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=REFERRAL_STATUS, default='new')
    
    def __str__(self):
        return f'{self.user.email}->{self.referrer.email}'


# class ReferalUsers(models.Model):
#     referal_link = models.ForeignKey(ReferalLink, on_delete=models.CASCADE)
#     children = models.ForeignKey(CandyUser, on_delete=models.CASCADE, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
