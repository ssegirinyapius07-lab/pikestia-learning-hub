from django.conf import settings
from django.db import migrations


def setup_pikestia_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site, _ = Site.objects.get_or_create(
        pk=settings.SITE_ID,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Pikestia Learning Hub',
        },
    )

    site.name = 'Pikestia Learning Hub'
    if site.domain == 'example.com':
        site.domain = '127.0.0.1:8000'
    site.save(update_fields=['name', 'domain'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(setup_pikestia_site, migrations.RunPython.noop),
    ]
