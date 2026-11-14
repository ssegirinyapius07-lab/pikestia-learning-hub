from django.contrib import admin

from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    def _is_admin(self, request):
        return bool(request.user.is_superuser or request.user.role == 'admin')

    def _is_publisher(self, request):
        return bool(not request.user.is_superuser and request.user.role == 'publisher')

    def has_module_permission(self, request):
        return self._is_admin(request) or self._is_publisher(request)

    def has_add_permission(self, request):
        return self._is_admin(request) or self._is_publisher(request)

    def has_view_permission(self, request, obj=None):
        if self._is_admin(request):
            return True
        if not self._is_publisher(request):
            return False
        return obj is None or obj.author_id == request.user.pk

    def has_change_permission(self, request, obj=None):
        if self._is_admin(request):
            return True
        if not self._is_publisher(request):
            return False
        return obj is None or obj.author_id == request.user.pk

    def has_delete_permission(self, request, obj=None):
        return self._is_admin(request)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self._is_publisher(request):
            return queryset.filter(author=request.user)
        return queryset

    def get_fieldsets(self, request, obj=None):
        if self._is_publisher(request):
            return (
                ('Article', {
                    'fields': (
                        'title',
                        'slug',
                        'category',
                        'summary',
                        'cover_image',
                        'body_raw',
                    ),
                    'description': (
                        'Publisher submissions enter review. An administrator must approve '
                        'an article before it becomes publicly visible.'
                    ),
                }),
                ('Sanitized preview', {
                    'fields': ('body',),
                    'classes': ('collapse',),
                }),
            )
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if self._is_publisher(request):
            obj.author = request.user
            obj.status = NewsArticle.Status.REVIEW
            obj.featured = False
            obj.published_at = None
        super().save_model(request, obj, form, change)

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
