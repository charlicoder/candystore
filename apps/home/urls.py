from django.urls import path
from django.views.generic.base import TemplateView
from .views import HomeView, AboutUsView, contact_us

app_name = 'apps.home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', contact_us, name='contact-us'),
]