from django.contrib import admin
from .models import LearningResource
@admin.register(LearningResource)
class LRAdmin(admin.ModelAdmin):
    list_display=('title','topic','status','order')
    list_filter=('status',)
    search_fields=('title','summary')
