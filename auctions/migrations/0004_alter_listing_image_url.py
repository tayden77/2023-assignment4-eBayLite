# Generated by Django 4.1.2 on 2023-10-25 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_category_listing_watchlist_comment_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='listing_images/'),
        ),
    ]
