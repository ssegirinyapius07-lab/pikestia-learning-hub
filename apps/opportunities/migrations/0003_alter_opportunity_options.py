from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opportunities', '0002_verification_publish_defaults'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opportunity',
            options={
                'verbose_name': 'Opportunity',
                'verbose_name_plural': 'Opportunities',
                'ordering': ['-published_at'],
            },
        ),
    ]
