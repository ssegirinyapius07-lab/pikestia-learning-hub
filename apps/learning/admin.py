from django.contrib import admin

from .models import LearningResource


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return bool(request.user.is_superuser or request.user.role in {'admin', 'publisher'})

    def has_add_permission(self, request):
        return bool(request.user.is_superuser or request.user.role in {'admin', 'publisher'})

    def has_change_permission(self, request, obj=None):
        return bool(request.user.is_superuser or request.user.role in {'admin', 'publisher'})

    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser or request.user.role == 'admin')

    def has_view_permission(self, request, obj=None):
        return bool(request.user.is_superuser or request.user.role in {'admin', 'publisher'})

    list_display = ('title', 'topic', 'is_featured', 'status', 'order', 'updated_at')
    list_filter = ('status', 'is_featured', 'topic__subject', 'topic__parent')
    search_fields = (
        'title',
        'summary',
        'objectives',
        'key_concepts',
        'content_raw',
        'topic__title',
        'topic__parent__title',
        'topic__subject__title',
        'topic__subject__discipline',
    )
    autocomplete_fields = ('topic',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('topic__subject__order', 'topic__subject__title', 'topic__parent__order', 'topic__order', 'order', 'title')
    list_select_related = ('topic', 'topic__subject', 'topic__parent')
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
                'Write a focused lesson with a clear explanation, worked examples, and a short recap. '
                'Use semantic HTML blocks such as <div class="study-block study-definition">...</div> '
                'for definitions, <div class="study-block study-formula">...</div> for formulas, '
                '<div class="study-block study-example">...</div> for worked examples, and tables for comparisons. '
                'Content is sanitized automatically before publication.'
            ),
        }),
        ('Sanitized content', {
            'fields': ('content',),
            'classes': ('collapse',),
        }),
        ('Publishing and discovery', {
            'fields': ('status', 'order', 'is_featured'),
            'description': (
                'Order lessons in the sequence students should follow. Feature only a small number of '
                'high-quality resources that are good entry points for learners.'
            ),
        }),
        ('System information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
