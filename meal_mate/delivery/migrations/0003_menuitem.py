# Generated by Django 5.1.4 on 2025-01-17 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=20)),
                ('item_description', models.TextField()),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('item_photo', models.URLField(default='https://cwdaust.com.au/wpress/wp-content/uploads/2015/04/placeholder-item.png', max_length=2000)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='delivery.restaurant')),
            ],
        ),
    ]
