from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
 list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
 list_filter = ('role', 'is_active', 'is_staff', 'created_at')
 search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id')
 ordering = ('-created_at',)
 
 fieldsets = (
 (None, {'fields': ('username', 'password')}),
 ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email', 'phone', 'student_id')}),
 ('مجوزها', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
 ('تاریخ‌های مهم', {'fields': ('last_login', 'created_at')}),
 )
 
 add_fieldsets = (
 (None, {
 'classes': ('wide',),
 'fields': ('username', 'email', 'password1', 'password2', 'role'),
 }),
 )
 
 readonly_fields = ('created_at',)