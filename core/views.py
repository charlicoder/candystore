from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView


from .forms import ContactForm


class AboutUsView(TemplateView):
    template_name = 'about-us.html'


def contact_us(request):
    import pdb; pdb.set_trace();
    form = ContactForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            data = form.cleaned_data
            subject = data['subject']
            message = data['message']

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      [data['recipient']])

    return render(request, 'contact-us.html', {'form': form})



