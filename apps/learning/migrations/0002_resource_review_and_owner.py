from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningresource',
            name='status',
            field=models.CharField(
                choices=[
                    ('draft', 'Draft'),
                    ('review', 'In Review'),
                    ('published', 'Published'),
                    ('archived', 'Archived'),
                ],
                default='draft',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='learningresource',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='learning_resources',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
