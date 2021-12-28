from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.views import LogoutView, LoginView
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from mlm.admin import marketing_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls'), name='home'),
    path('dashboard/', include('apps.dashboard.urls'), name='dashboard'),
    path('users/', include('apps.users.urls')),
    path('mlm/', include('apps.mlm.urls')),
    
    # path('marketing', marketing_site.site.urls),
    
    # path('login/', LoginView.as_view(), name='test-login'),
    # path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    # path('register/', SignUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
    )
