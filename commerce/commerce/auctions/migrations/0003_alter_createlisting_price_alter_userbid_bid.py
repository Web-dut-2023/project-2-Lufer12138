# Generated by Django 4.2.4 on 2023-08-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_userbid_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createlisting',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userbid',
            name='bid',
            field=models.IntegerField(),
        ),
    ]
