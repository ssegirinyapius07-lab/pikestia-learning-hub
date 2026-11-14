from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_setup_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('user', 'User'),
                    ('admin', 'Administrator'),
                    ('publisher', 'Publisher'),
                ],
                default='user',
                max_length=20,
            ),
        ),
    ]
