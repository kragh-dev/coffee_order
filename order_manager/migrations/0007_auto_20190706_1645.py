# Generated by Django 2.2.3 on 2019-07-06 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0006_items_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_phone',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_status',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='otp',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ordertemplate',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user_phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(),
        ),
    ]