from django.contrib import admin
from .models import Subject, Topic
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display=('title','discipline','status','order')
    prepopulated_fields={'slug':('title',)}
    list_filter=('discipline','status')
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display=('title','subject','status','order')
    list_filter=('subject','status')
    prepopulated_fields={'slug':('title',)}
