from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newsarticle_cover_image'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='newsarticle',
            old_name='news_newsart_status_1d9a9e_idx',
            new_name='news_newsar_status_0d9faa_idx',
        ),
        migrations.RenameIndex(
            model_name='newsarticle',
            old_name='news_newsart_categor_ae8903_idx',
            new_name='news_newsar_categor_378b25_idx',
        ),
        migrations.RenameIndex(
            model_name='newsarticle',
            old_name='news_newsart_author_8ba9e3_idx',
            new_name='news_newsar_author__e70620_idx',
        ),
        migrations.RenameIndex(
            model_name='newsarticle',
            old_name='news_newsart_featur_5bb4d0_idx',
            new_name='news_newsar_feature_e833e4_idx',
        ),
    ]
