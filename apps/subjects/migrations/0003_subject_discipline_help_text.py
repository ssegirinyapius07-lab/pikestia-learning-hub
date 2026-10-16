from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_topic_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='discipline',
            field=models.CharField(
                help_text='Academic group or branch, e.g. Science & Technology or Business.',
                max_length=100,
            ),
        ),
    ]
