from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    fieldsets = (
        ('Login Credentials', {'fields': ('username', 'password')}),
        ('Personal Details', {'fields': ('first_name', 'last_name', 'phone', 'dob', 'gender')}),
        ('Profile Details', {'fields': ('email', 'facebook_url', 'instagram_url', 'twitter_url',)}),
        ('Other Details', {'fields': ('date_joined', 'is_active', 'is_staff')}),
    )
    add_fieldsets = (
        ('Login Credentials', {'fields': ('username', 'password')}),
        ('Personal Details', {'fields': ('first_name', 'last_name', 'phone', 'dob', 'gender')}),
        ('Profile Details', {'fields': ('email', 'facebook_url', 'instagram_url', 'twitter_url',)}),
        ('Other Details', {'fields': ('date_joined', 'is_active', 'is_staff')}),
    )
    
    ordering = ('username',)
    search_fields = ['username']
    list_filter = ['is_active', 'is_staff']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('username', )
        return self.readonly_fields

admin.site.register(User, UserAdmin)

admin.site.site_title = "Blog Management System - by Yuvi Jadeja"
admin.site.site_header = "Blogs | by Yuvi Jadeja"