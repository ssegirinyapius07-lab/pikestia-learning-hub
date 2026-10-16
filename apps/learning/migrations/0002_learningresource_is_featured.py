import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
        ('subjects', '0002_topic_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningresource',
            name='is_featured',
            field=models.BooleanField(
                default=False,
                help_text='Feature this published material in Pikestia recommendations and the homepage.',
            ),
        ),
        migrations.AddIndex(
            model_name='learningresource',
            index=models.Index(fields=['is_featured', 'status'], name='learning_res_featured_status_idx'),
        ),
    ]
