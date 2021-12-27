from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from users.forms import SignUpForm, IdVerifyForm
from users.models import CandyUser, CandyUserProfile, UserEmailVeirfyToken
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from mlm.models import ReferalCode, CandyUserReferral
from django.contrib import  messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .tokens import account_activation_token
import idanalyzer
from django.contrib.auth import authenticate, login

def say_hello(request):
    import pdb; pdb.set_trace()
    
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
    success_url = reverse_lazy('login')
    form_class = SignUpForm

    # def get(self, request):
    #     return render(request, 'users/signup.html')

    def form_valid(self, form):
        # import pdb; pdb.set_trace();
        rcode = self.kwargs.get('code')

        if not rcode:
            raise ValueError('Sorry! you can not signup without rafarral...!')
        
        try:
            rc = ReferalCode.objects.get(token=rcode)

            form = form.save(commit=False)
            form.status = 'new'
            form.is_active = False
            form.save()
            
            candy_user_referral = CandyUserReferral.objects.create(
                parent=rc.created_by,
                referral_code=rc,
                child=form,
                status='new'
            )

            # send email with email verification link
            user = form
            current_site = get_current_site(self.request)
            to_email = form.email
            mail_subject = 'Activate your account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            message = render_to_string('users/email_activation_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            # import pdb; pdb.set_trace();
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            # UserEmailVeirfyToken.objects.create(user=form, token=token, status='new')

            # messages.SUCCESS(request, 'Email verification link is sent. Please check your email.')
            
        except Exception as e:
            # raise ValueError('Sorry! you can not signup without rafarral...!')
            messages.ERROR(request, 'Signup process error!')
            return render(self.request, 'error.html', {'error_note': 'Invalide referral code!'})
        
        return redirect(reverse_lazy('about-us'))


class VerifyEmailView(View):
    
    def get(self, request, uidb64, token):
        # return redirect(reverse_lazy('users:id-verify'))
        # import pdb; pdb.set_trace()
        # User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CandyUser.objects.get(pk=uid)
            # uid2 = UserEmailVeirfyToken.objects.get(token=token).user.uid
            # user2 = CandyUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CandyUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.status = 'email_verified'
            user.save()
            login(request, user)
            return redirect(reverse_lazy('users:id-verify'))
            # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


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
        document_primary = files['nid'].temporary_file_path()
        biometric_photo = files['avater'].temporary_file_path()

        try:
            response = coreapi.scan(document_primary=document_primary, biometric_photo=biometric_photo)
            data = response['result']
            if response.get('authentication'):
                authentication_result = response['authentication']
                if authentication_result['score'] > 0.5:
                    print("The document uploaded is authentic")
                    first_name = data['firstName']
                    last_name = data['lastName']
                else:
                    request.user.status = 'id_not_verified'
                    request.user.save()
                    return redirect(reverse_lazy('about-us'))
            
            # Parse biometric verification results
            if response.get('face'):
                face_result = response['face']
                if face_result['isIdentical']:
                    print("Face verification PASSED!")
                    
                else:
                    print("Face verification FAILED!")
                    request.user.status = 'id_not_verified'
                    request.user.save()
                    return redirect(reverse_lazy('about-us'))

                print("Confidence Score: " + face_result['confidence'])
            
            import pdb; pdb.set_trace()

            profile = CandyUserProfile(
                user = request.user,
                first_name = first_name, 
                last_name = last_name, 
                avater = request.FILES['avater']
            )
            # profile.user = request.user 
            # profile.avater = face_result
            # profile.first_name = first_name
            # profile.last_name = last_name
            profile.save()
            request.user.status = 'id_verified'
            request.user.save()
            return redirect(reverse_lazy('users:agreement'))
        except Exception as e:
            print(e)
        

class SignupAgreementView(View):

    def get(self, request):
        context = {}
        return render(request, 'users/agreement.html', context)
    
    def post(self, request):
        # import pdb; pdb.set_trace()
        request.user.status = 'active'
        request.user.save()
        return redirect(reverse_lazy('dashboard'))


class CandyUserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm
    success_url = '/dashboard/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        # import pdb; pdb.set_trace()
        user = form.get_user()
        login(self.request, user)
        if user.status == 'active':
            return redirect(reverse_lazy('dashboard'))
        else:
            return redirect(reverse_lazy('about-us'))


class CandyUserProfile(DetailView):
    model = CandyUser
    template_name = 'users/candyuserprofile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.candyuserprofile
        return context

    # def form_valid(self, form):
