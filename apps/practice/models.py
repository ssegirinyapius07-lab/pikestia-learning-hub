from django.db import models
class PracticeQuestion(models.Model):
    class QType(models.TextChoices):
        MCQ='mcq','Multiple Choice'
        SHORT='short','Short Answer'
        EXERCISE='exercise','Exercise'
    class Status(models.TextChoices):
        DRAFT='draft','Draft'
        PUBLISHED='published','Published'
        ARCHIVED='archived','Archived'
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=20, choices=QType.choices, default=QType.MCQ)
    question = models.TextField()
    options = models.JSONField(default=list, blank=True, help_text="For MCQ: list of strings")
    correct_answer = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, default='medium')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']
        indexes=[models.Index(fields=['status']), models.Index(fields=['type'])]

    def __str__(self): return self.question[:80]
