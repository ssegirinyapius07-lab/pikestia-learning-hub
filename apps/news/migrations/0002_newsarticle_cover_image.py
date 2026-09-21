from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='cover_image',
            field=models.ImageField(
                blank=True,
                help_text='Optional cover image used in the newsroom and featured story cards.',
                upload_to='news/covers/',
            ),
        ),
    ]
