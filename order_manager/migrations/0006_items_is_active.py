# Generated by Django 2.2.3 on 2019-07-06 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0005_user_shop_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
