# Generated by Django 5.0.2 on 2024-03-04 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_user_image_verificationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationcode',
            name='token',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]