from django.contrib import admin
from .models import Opportunity
@admin.register(Opportunity)
class OppAdmin(admin.ModelAdmin):
    list_display=('title','category','status','is_verified','deadline','published_at')
    list_filter=('category','status','is_verified')
    prepopulated_fields={'slug':('title',)}
    search_fields=('title','description')
