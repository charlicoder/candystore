from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from .forms import SignUpForm, IdVerifyForm
from .models import CandyUser, CandyUserProfile
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from apps.mlm.models import ReferralCode, ReferralUserProfile
from django.contrib import  messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin

import idanalyzer

from .tokens import account_activation_token
from django.contrib.auth import authenticate, login as auth_login


def say_hello(request):
    user = request.user
    subject = 'Activate your account.'
    current_site = get_current_site(request)
    message = render_to_string('email_template.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    user.email_user(subject, message)

    return render(request, 'users/index.html', {'token': 'hfklasjhlksjhadflkahs'})


class HomeView(View):

    def get(self, request):
        # import pdb; pdb.set_trace();
        # pdb.set_trace()
        mail_subject = 'Activate your account.'
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(request.user.pk))
        token = account_activation_token.make_token(request.user)
        activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
        message = "Hello {0},\n {1}".format(request.user.username, activation_link)
        to_email = 'mamun1980@gmail.com'
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return render(request, 'users/index.html', {'token': token, 'uid': uid})


class SignUpView(CreateView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')
    form_class = SignUpForm

    # def get(self, request):
    #     return render(request, 'users/signup.html')

    def form_valid(self, form):
        rcode = self.kwargs.get('code')
        # import pdb;
        # pdb.set_trace();

        if not rcode:
            raise ValueError('Sorry! you can not signup without referral...!')

        try:
            rc = ReferralCode.objects.get(token=rcode)

        except ReferralCode.DoesNotExist:
            messages.error(self.request, 'Your referral code is not valid')
            return redirect(reverse_lazy('users:signup'))

        
        try:
            candy_user = form.save(commit=False)
            candy_user.status = 'new'
            candy_user.is_active = False
            candy_user.save()

            # Create CandyUserProfile object
            CandyUserProfile.objects.create(user=candy_user)

            # Create referral_user_profile object
            ReferralUserProfile.objects.create(
                referrer=rc.created_by,
                referral_code=rc,
                user=candy_user,
                status='new'
            )

            rc.users_count += 1
            rc.save()

            # send email with email verification link
            current_site = get_current_site(self.request)
            to_email = candy_user.email
            mail_subject = 'Activate your account.'
            uid = urlsafe_base64_encode(force_bytes(candy_user.pk))
            token = account_activation_token.make_token(candy_user)

            message = render_to_string('users/email_activation_template.html', {
                'user': candy_user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            # import pdb; pdb.set_trace();
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            # UserEmailVeirfyToken.objects.create(user=form, token=token, status='new')

            messages.success(self.request, 'Email verification link is sent. Please check your email & click verification '
                                      'link to complete the signup process.')

        except Exception as e:
            messages.error(self.request, 'Signup process error!')

        return redirect(reverse_lazy('home:contact'))


class VerifyEmailView(View):
    
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CandyUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CandyUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.status = 'email_verified'
            user.save()
            auth_login(request, user)
            return redirect(reverse_lazy('users:id-verify'))
        else:
            messages.error(request, 'Email verification process error!')
            return redirect(reverse_lazy('home:contact'))


class IdVerifyView(View):

    def get(self, request):
        form = IdVerifyForm()
        context = {'form': form}
        return render(request, 'users/id-verify.html', context)

    def post(self, request):
        files = request.FILES
        
        coreapi = idanalyzer.CoreAPI("F0r5vzpkU4H908WuSsVMaZRmOrtGfUJu", "US")
        # Raise exceptions for API level errors
        coreapi.throw_api_exception(True)
        # enable document authentication using quick module
        coreapi.enable_authentication(True, 'quick')
        coreapi.enable_authentication(True, 2)
        document_nid = files['nid'].temporary_file_path()
        photo = files['avatar'].temporary_file_path()

        try:
            response = coreapi.scan(document_primary=document_nid, biometric_photo=photo)
            data = response['result']
            profile = request.user.candyuserprofile

            if response.get('authentication'):
                authentication_result = response['authentication']
                if authentication_result['score'] > 0.5:
                    first_name = data['firstName']
                    last_name = data['lastName']
                else:
                    request.user.status = 'id_not_verified'
                    request.user.save()
                    return redirect(reverse_lazy('home:contact'))
            
            # Parse biometric verification results
            if response.get('face'):
                face_result = response['face']
                if not face_result['isIdentical']:
                    request.user.status = 'id_not_verified'
                    request.user.save()
                    return redirect(reverse_lazy('home:contact'))


            # import pdb; pdb.set_trace()

            profile.avatar = files['avatar']
            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()
            # profile.avater = face_result
            # profile.first_name = first_name
            # profile.last_name = last_name

            request.user.status = 'id_verified'
            request.user.save()
            messages.success(request, 'your document is verified successfully')

        except Exception as e:
            return redirect(reverse_lazy('home:contact'))

        return redirect(reverse_lazy('users:agreement'))
        

class SignupAgreementView(View):

    def get(self, request):
        context = {}
        return render(request, 'users/agreement.html', context)
    
    def post(self, request):
        # import pdb; pdb.set_trace()
        request.user.status = 'active'
        request.user.save()
        return redirect(reverse_lazy('dashboard:home'))


class CandyUserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm
    

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        auth_login(self.request, user)

        '''
        Todo: check signup status if all steps are complete. If not redirect to the last step not completed.
        If completed the redirect to dashboard.
        '''

        # return redirect(reverse_lazy('dashboard:home'))

        if user.status == 'active':
            return redirect(reverse_lazy('dashboard:home'))
        elif user.status == 'email_verified':
            return redirect(reverse_lazy('users:id-verify'))
        elif user.status == 'doc_verified':
            return redirect(reverse_lazy('users:agreement'))
        else:
            return redirect(reverse_lazy('home:home'))




class CandyUserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class CandyUserProfileV2(LoginRequiredMixin, TemplateView):
    template_name = 'users/candyuserprofile-v2.html'


# class CandyUserProfile(DetailView):
#     model = CandyUser
#     template_name = 'users/candyuserprofile_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['profile'] = self.object.candyuserprofile
#         return context

    # def form_valid(self, form):
