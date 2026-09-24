from django.contrib import admin

from .models import User, AuditLog, CookiePreference
from apps.core.admin_permissions import AdminOnlyModelAdmin


@admin.register(User)
class UserAdmin(AdminOnlyModelAdmin):
    list_display = ('email', 'full_name', 'role', 'display_mode', 'is_active', 'date_joined')
    list_filter = ('role', 'display_mode', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)


@admin.register(AuditLog)
class AuditLogAdmin(AdminOnlyModelAdmin):
    list_display = ('action', 'user', 'ip_address', 'created_at')
    list_filter = ('action',)
    readonly_fields = ('user', 'action', 'ip_address', 'user_agent', 'metadata', 'created_at')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CookiePreference)
class CookiePrefAdmin(AdminOnlyModelAdmin):
    list_display = ('user', 'session_key', 'analytics', 'marketing', 'updated_at')
