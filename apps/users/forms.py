from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CandyUser
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    
    class Meta:
        model = CandyUser
        fields = [
            'email', 
            'password1', 
            'password2', 
        ]


class IdVerifyForm(forms.Form):
    nid = forms.ImageField()
    avater = forms.ImageField()





'''

class RegistrationForm(UserCreationForm):

    class Meta:
        model = CandyUser
        fields = ('email', 'password1', 'password2',)
    

    def clean(self):
        """
        Verifies that the values entered into the password fields match
        NOTE : errors here will appear in 'non_field_errors()'
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please try again!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CandyUser
        fields = ('email', 'first_name', 'last_name',)

'''
