# Generated by Django 2.2.3 on 2019-07-06 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0003_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
