from django.contrib import admin

from .models import LearningResource


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'status', 'order', 'updated_at')
    list_filter = ('status', 'topic__subject')
    search_fields = (
        'title',
        'summary',
        'key_concepts',
        'topic__title',
        'topic__subject__title',
    )
    autocomplete_fields = ('topic',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('topic__subject__title', 'topic__order', 'order', 'title')
    list_select_related = ('topic', 'topic__subject')
    list_per_page = 25
    date_hierarchy = 'updated_at'
    readonly_fields = ('content', 'created_at', 'updated_at')

    fieldsets = (
        ('Learning material', {
            'fields': (
                'topic',
                'title',
                'slug',
                'summary',
                'objectives',
                'key_concepts',
                'content_raw',
            ),
            'description': (
                'Enter the source learning content as HTML. Use semantic blocks such as '
                '<div class="study-block study-definition">...</div> for definitions, '
                '<div class="study-block study-formula">...</div> for formulas, '
                '<div class="study-block study-example">...</div> for worked examples, '
                'and regular tables for calculations. Content is sanitized automatically before publication.'
            ),
        }),
        ('Sanitized content', {
            'fields': ('content',),
            'classes': ('collapse',),
        }),
        ('Publishing', {
            'fields': ('status', 'order'),
        }),
        ('System information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
