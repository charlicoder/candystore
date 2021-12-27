from django import forms


class ContactForm(forms.Form):
    recipient = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

