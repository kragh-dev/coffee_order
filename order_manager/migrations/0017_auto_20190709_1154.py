# Generated by Django 2.2.3 on 2019-07-09 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0016_auto_20190709_0213'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Automate',
        ),
        migrations.RemoveField(
            model_name='orderlist',
            name='price',
        ),
        migrations.AddField(
            model_name='schedule',
            name='evening_schedule',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='morning_schedule',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
