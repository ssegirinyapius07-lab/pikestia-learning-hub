from django.contrib import admin

from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
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
    list_display = (
        'title',
        'category',
        'author',
        'status',
        'featured',
        'published_at',
        'updated_at',
    )
    list_filter = ('category', 'status', 'featured')
    search_fields = (
        'title',
        'summary',
        'body_raw',
        'author__email',
        'author__full_name',
    )
    autocomplete_fields = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    list_select_related = ('author',)
    ordering = ('-published_at', '-created_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ('body', 'created_at', 'updated_at')

    fieldsets = (
        ('Article', {
            'fields': (
                'title',
                'slug',
                'category',
                'author',
                'summary',
                'cover_image',
                'body_raw',
            ),
            'description': (
                'Write the article in HTML. The source is sanitized '
                'automatically before public display.'
            ),
        }),
        ('Publishing', {
            'fields': (
                'status',
                'featured',
                'published_at',
            ),
        }),
        ('Sanitized body', {
            'fields': ('body',),
            'classes': ('collapse',),
        }),
        ('System information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
