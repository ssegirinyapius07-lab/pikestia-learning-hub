from django.contrib import admin

from .models import LearningResource


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
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
        return obj is None or obj.created_by_id == request.user.pk

    def has_change_permission(self, request, obj=None):
        if self._is_admin(request):
            return True
        if not self._is_publisher(request):
            return False
        return obj is None or obj.created_by_id == request.user.pk

    def has_delete_permission(self, request, obj=None):
        return self._is_admin(request)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self._is_publisher(request):
            return queryset.filter(created_by=request.user)
        return queryset

    def get_fieldsets(self, request, obj=None):
        if self._is_publisher(request):
            return (
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
                        'Submit clear, accurate learning material. Publisher submissions '
                        'enter review and are not published until an administrator approves them.'
                    ),
                }),
            )
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if self._is_publisher(request):
            obj.created_by = request.user
            obj.status = LearningResource.Status.REVIEW
        super().save_model(request, obj, form, change)

    list_display = ('title', 'topic', 'status', 'created_by', 'order', 'updated_at')
    list_filter = ('status', 'topic__subject')
    search_fields = (
        'title',
        'summary',
        'key_concepts',
        'topic__title',
        'topic__subject__title',
        'created_by__email',
    )
    autocomplete_fields = ('topic',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('topic__subject__title', 'topic__order', 'order', 'title')
    list_select_related = ('topic', 'topic__subject', 'created_by')
    list_per_page = 25
    date_hierarchy = 'updated_at'
    readonly_fields = ('content', 'created_by', 'created_at', 'updated_at')

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
        ('Publishing', {
            'fields': ('status', 'order'),
        }),
        ('Sanitized content', {
            'fields': ('content',),
            'classes': ('collapse',),
        }),
        ('System information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
