from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home/index.html'

class AboutUsView(TemplateView):
    template_name = 'about-us.html'


def contact_us(request):
    # import pdb; pdb.set_trace();
    form = ContactForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            data = form.cleaned_data
            subject = data['subject']
            message = data['message']

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      [data['recipient']])

    return render(request, 'home/contact-us.html', {'form': form})