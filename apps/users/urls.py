from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from .views import ( SignUpView, CandyUserLoginView, 
            VerifyEmailView, HomeView, IdVerifyView, 
            SignupAgreementView, CandyUserProfileView
        )

app_name = 'users'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/<str:code>/', SignUpView.as_view(), name='signup'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    # path('verify-email/<uidb64>/<token>/', activate, name='active'),
    path('id-verify/', IdVerifyView.as_view(), name='id-verify'),
    path('signup-agreement/', SignupAgreementView.as_view(), name='agreement'),
    path('login/', CandyUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('<int:pk>/profile-v1/', CandyUserProfileView.as_view(), name='profile'),
]
