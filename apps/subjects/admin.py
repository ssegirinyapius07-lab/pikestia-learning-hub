from django.contrib import admin

from .models import Subject, Topic
from apps.core.admin_permissions import AdminOnlyModelAdmin


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0
    fields = ('title', 'slug', 'status', 'order')
    prepopulated_fields = {'slug': ('title',)}
    show_change_link = True
    ordering = ('order', 'title')


@admin.register(Subject)
class SubjectAdmin(AdminOnlyModelAdmin):
    list_display = ('title', 'discipline', 'status', 'topic_count', 'order')
    list_filter = ('discipline', 'status')
    search_fields = ('title', 'description', 'discipline')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')
    list_per_page = 25
    inlines = (TopicInline,)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'discipline', 'icon', 'order', 'status'),
        }),
        ('System information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Topics', ordering='topic_count')
    def topic_count(self, obj):
        return obj.topics.count()


@admin.register(Topic)
class TopicAdmin(AdminOnlyModelAdmin):
    list_display = ('title', 'subject', 'status', 'resource_count', 'order')
    list_filter = ('subject', 'status')
    search_fields = ('title', 'summary', 'learning_objectives', 'subject__title')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('subject',)
    ordering = ('subject', 'order', 'title')
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('subject', 'title', 'slug', 'summary', 'learning_objectives'),
        }),
        ('Publishing', {
            'fields': ('status', 'order'),
        }),
        ('System information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Materials', ordering='resource_count')
    def resource_count(self, obj):
        return obj.resources.count()
