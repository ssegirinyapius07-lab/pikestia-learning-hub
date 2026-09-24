from django.contrib import admin

from .models import Opportunity
from apps.core.admin_permissions import AdminOnlyModelAdmin


@admin.register(Opportunity)
class OppAdmin(AdminOnlyModelAdmin):
    list_display = ('title', 'category', 'status', 'is_verified', 'deadline', 'published_at')
    list_filter = ('category', 'status', 'is_verified')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
