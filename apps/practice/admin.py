from django.contrib import admin

from .models import PracticeQuestion


@admin.register(PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'topic', 'type', 'difficulty', 'status', 'created_at')
    list_filter = ('type', 'status', 'difficulty', 'topic__subject')
    search_fields = (
        'question',
        'correct_answer',
        'explanation',
        'topic__title',
        'topic__subject__title',
    )
    autocomplete_fields = ('topic',)
    list_select_related = ('topic', 'topic__subject')
    ordering = ('topic__subject__title', 'topic__order', 'id')
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Question', {
            'fields': ('topic', 'type', 'question', 'options'),
        }),
        ('Answer and feedback', {
            'fields': ('correct_answer', 'explanation'),
            'description': (
                'For multiple-choice questions, options should be a JSON list '
                'of answer strings. Keep the correct answer out of the question text.'
            ),
        }),
        ('Publishing', {
            'fields': ('difficulty', 'status'),
        }),
        ('System information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at',)

    @admin.display(description='Question')
    def question_preview(self, obj):
        return obj.question[:90]
