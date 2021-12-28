from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CandyUser, UserEmailVeirfyToken, CandyUserProfile
# from .forms import RegistrationForm, CustomUserChangeForm
from django.utils.safestring import mark_safe

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'is_active', 'status', 'parent_user_email', 'list_child')

    def first_name(self, obj):
        return obj.candyuserprofile.first_name
    
    def last_name(self, obj):
        return obj.candyuserprofile.last_name
    
    def parent_user_email(self, obj):
        if obj.child.first() is not None:
            parent = obj.child.first().parent
        else:
            parent = None
        if parent is None:
            return 'None'
        else:
            return parent.email
            
    
    def list_child(self, obj):
        return mark_safe(f'<a href="/about-us">Child List</a>')
    
    list_child.allow_tags = True

    
    # def first_name(self, obj):
    #     return obj.candyuserprofile.first_name

    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = CandyUser
    # list_display = ('id', 'candyuser__user',)
    # list_filter = ('is_staff',)
    # fieldsets = ((None, 
    #               {'fields':('email','password', 'first_name', 'last_name')}), ('Permissions',{'fields':('is_staff',)}),)
    # add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'first_name', 'last_name')}),)
    # search_fields =('email',)
    # ordering = ('email',)
    # filter_horizontal = ()

admin.site.register(CandyUser, UserAdmin)
admin.site.unregister(Group)

class CandyUserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'avater', 'user')

admin.site.register(CandyUserProfile, CandyUserProfileAdmin)


class UserEmailVeirfyTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'status')


admin.site.register(UserEmailVeirfyToken, UserEmailVeirfyTokenAdmin)
