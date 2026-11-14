from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='status',
            field=models.CharField(
                choices=[
                    ('draft', 'Draft'),
                    ('active', 'Active'),
                    ('expired', 'Expired'),
                    ('archived', 'Archived'),
                ],
                default='draft',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
