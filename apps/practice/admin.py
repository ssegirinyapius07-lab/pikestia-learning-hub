from django.contrib import admin
from .models import PracticeQuestion
@admin.register(PracticeQuestion)
class PQAdmin(admin.ModelAdmin):
    list_display=('question','topic','type','status','difficulty')
    list_filter=('type','status','difficulty')
