# Generated by Django 2.2.3 on 2019-07-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0007_auto_20190706_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='user_phone',
            new_name='phone',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]