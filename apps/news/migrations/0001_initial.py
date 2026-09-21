from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=280, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('summary', models.TextField(blank=True)),
                ('body', models.TextField(help_text='Sanitized HTML')),
                ('body_raw', models.TextField(blank=True, help_text='Original article HTML before sanitization')),
                ('category', models.CharField(choices=[('campus', 'Campus'), ('academic', 'Academic'), ('technology', 'Technology'), ('career', 'Career'), ('community', 'Community'), ('general', 'General')], default='general', max_length=20)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('review', 'In Review'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('featured', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news_articles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-published_at', '-created_at'],
                'indexes': [
                    models.Index(fields=['status', '-published_at'], name='news_newsart_status_1d9a9e_idx'),
                    models.Index(fields=['category', '-published_at'], name='news_newsart_categor_ae8903_idx'),
                    models.Index(fields=['author', '-created_at'], name='news_newsart_author_8ba9e3_idx'),
                    models.Index(fields=['featured', '-published_at'], name='news_newsart_featur_5bb4d0_idx'),
                ],
            },
        ),
    ]
