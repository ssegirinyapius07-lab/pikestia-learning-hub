from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_bookmark_integrity'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='bookmark',
            name='bookmark_exactly_one_target',
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.CheckConstraint(
                condition=(
                    Q(resource__isnull=False, topic__isnull=True, opportunity__isnull=True)
                    | Q(resource__isnull=True, topic__isnull=False, opportunity__isnull=True)
                    | Q(resource__isnull=True, topic__isnull=True, opportunity__isnull=False)
                ),
                name='bookmark_exactly_one_target',
            ),
        ),
    ]
