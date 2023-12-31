# Generated by Django 2.1.10 on 2023-12-19 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='email',
            field=models.CharField(default='1048655155@qq.com', max_length=64, verbose_name='邮箱'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admin',
            name='phone',
            field=models.CharField(default=1, max_length=64, verbose_name='电话号码'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=20, verbose_name='年龄'),
        ),
    ]
