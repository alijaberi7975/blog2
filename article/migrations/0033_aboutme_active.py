# Generated by Django 5.0.2 on 2024-03-05 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0032_contactus_checked_alter_contactus_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutme',
            name='active',
            field=models.BooleanField(default=False, verbose_name='وضعیت'),
        ),
    ]
