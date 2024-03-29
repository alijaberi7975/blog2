# Generated by Django 5.0.2 on 2024-03-05 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0031_favoritearticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='بررسی شده'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='Name',
            field=models.CharField(max_length=30, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='body',
            field=models.TextField(verbose_name='متن درخواست'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='شماره تلفن'),
        ),
    ]
