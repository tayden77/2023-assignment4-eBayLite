# Generated by Django 4.1.2 on 2023-10-30 19:28

from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('auctions', 'Category')
    categories = [
    'Antiques',
    'Art',
    'Books',
    'Business & Industrial',
    'Cameras & Photo',
    'Cell Phones & Accessories',
    'Clothing, Shoes & Accessories',
    'Collectibles',
    'Computers/Tablets & Networking',
    'Consumer Electronics',
    'Crafts',
    'DVDs & Movies',
    'Gift Cards & Coupons',
    'Health & Beauty',
    'Home & Garden',
    'Jewelry & Watches',
    'Music',
    'Musical Instruments & Gear',
    'Pet Supplies',
    'Pottery & Glass',
    'Sporting Goods',
    'Sports Mem, Cards & Fan Shop',
    'Tickets & Experiences',
    'Toys & Hobbies',
    'Travel',
    'Video Games & Consoles',
]
    for category_name in categories:
        Category.objects.create(name=category_name)

class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories)
    ]
