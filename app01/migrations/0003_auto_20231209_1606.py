# Generated by Django 2.1.10 on 2023-12-09 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20231208_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateField(verbose_name='入职时间'),
        ),
    ]
