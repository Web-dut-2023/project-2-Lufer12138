# Generated by Django 4.2.4 on 2023-08-15 11:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_createlisting_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createlisting',
            name='WatchList',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
