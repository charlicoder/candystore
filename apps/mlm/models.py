from django.db import models
from apps.users.models import CandyUser
import secrets

REFERAL_STATUS = (('active', 'Active'), ('inactive', 'Inactive'), ('new', 'New'))


# Create your models here.
class ReferalCode(models.Model):
    created_by = models.ForeignKey(CandyUser, on_delete=models.CASCADE, editable=False)
    token = models.CharField(max_length=100, blank=False, null=False, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REFERAL_STATUS, default='new')
    

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if self.id is None:
            token = secrets.token_urlsafe(32)
            self.token = token
            self.created_by = self.request.user

        super().save(*args, **kwargs)
        

class CandyUserReferral(models.Model):
    parent = models.ForeignKey(CandyUser, editable=False, on_delete=models.CASCADE, blank=False, null=False, related_name='parent')
    referral_code = models.ForeignKey(ReferalCode, editable=False, on_delete=models.CASCADE, blank=False, null=False)
    child = models.ForeignKey(
        CandyUser, editable=False, on_delete=models.CASCADE, blank=False, null=False, related_name='child')

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=REFERAL_STATUS, default='new')
    
    def __str__(self):
        return f'{self.parent.email}->{self.child.email}'


# class ReferalUsers(models.Model):
#     referal_link = models.ForeignKey(ReferalLink, on_delete=models.CASCADE)
#     children = models.ForeignKey(CandyUser, on_delete=models.CASCADE, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
