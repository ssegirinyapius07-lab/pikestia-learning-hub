from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opportunities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opportunity',
            options={
                'ordering': ['-published_at'],
                'verbose_name': 'Opportunity',
                'verbose_name_plural': 'Opportunities',
            },
        ),
    ]
