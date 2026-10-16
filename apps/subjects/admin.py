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
    verbose_name = 'Top-level topic'
    verbose_name_plural = 'Top-level topics'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)


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
            'description': (
                'Use Discipline for the broad academic group, such as Science & Technology. '
                'Use the Subject title for the branch, such as Information Technology.'
            ),
        }),
        ('System information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Top-level topics')
    def topic_count(self, obj):
        return obj.topics.filter(parent__isnull=True).count()


@admin.register(Topic)
class TopicAdmin(AdminOnlyModelAdmin):
    list_display = ('title', 'subject', 'parent', 'status', 'resource_count', 'order')
    list_filter = ('subject', 'parent', 'status')
    search_fields = (
        'title',
        'summary',
        'learning_objectives',
        'subject__title',
        'subject__discipline',
        'parent__title',
    )
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('subject',)
    ordering = ('subject', 'parent__order', 'parent__title', 'order', 'title')
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Topic structure', {
            'fields': ('subject', 'parent', 'title', 'slug', 'summary', 'learning_objectives'),
            'description': (
                'Leave Parent topic empty for a main topic such as Web Design. '
                'Choose a main topic for grouped subtopics such as HTML, CSS and JavaScript. '
                'Keep Order consistent with the intended learning sequence.'
            ),
        }),
        ('Publishing', {
            'fields': ('status', 'order'),
        }),
        ('System information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            parents = Topic.objects.filter(parent__isnull=True).select_related('subject')
            subject_id = request.POST.get('subject') or request.GET.get('subject')

            if not subject_id and getattr(request, 'resolver_match', None):
                object_id = request.resolver_match.kwargs.get('object_id')
                if object_id:
                    current = Topic.objects.filter(pk=object_id).only('subject_id').first()
                    if current:
                        subject_id = current.subject_id

            if subject_id and str(subject_id).isdigit():
                parents = parents.filter(subject_id=subject_id)

            kwargs['queryset'] = parents

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='Published materials')
    def resource_count(self, obj):
        return obj.resources.filter(status='published').count()
