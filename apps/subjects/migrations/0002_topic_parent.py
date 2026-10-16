# Generated for the nested learning catalogue.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                help_text='Optional parent topic. Use this to group lessons, for example Web Design → HTML Fundamentals.',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='children',
                to='subjects.topic',
            ),
        ),
        migrations.AddIndex(
            model_name='topic',
            index=models.Index(fields=['parent', 'order'], name='subjects_to_parent_order_idx'),
        ),
    ]
