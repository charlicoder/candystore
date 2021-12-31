from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CandyUser, CandyUserProfile
from .forms import CandyUserCreationForm, CandyUserChangeForm
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class CandyUserAdmin(admin.ModelAdmin):
    add_form = CandyUserChangeForm
    form = CandyUserCreationForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # obj.created_by = request.user
        CandyUserProfile.objects.create(user=obj)



    list_display = ('id', 'email', 'is_active', 'status', 'list_child')

    def first_name(self, obj):
        return obj.first_name
    
    def last_name(self, obj):
        return obj.last_name
    
    # def parent_user_email(self, obj):
    #     if obj.child.first() is not None:
    #         parent = obj.child.first().parent
    #     else:
    #         parent = None
    #     if parent is None:
    #         return 'None'
    #     else:
    #         return parent.email
    #
    # parent_user_email.allow_tags = True
            
    
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

admin.site.register(CandyUser, CandyUserAdmin)
admin.site.unregister(Group)


class CandyUserProfileAdmin(admin.ModelAdmin):

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="80" />'.format(obj.avatar.url))
        else:
            return format_html('<img src="/static/assets/images/placeholder.png" width="80" />')

    avatar_preview.short_description = 'Image'

    list_display = ('id', 'user', 'avatar_preview')


admin.site.register(CandyUserProfile, CandyUserProfileAdmin)


