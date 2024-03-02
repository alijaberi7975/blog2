# Generated by Django 5.0.2 on 2024-02-10 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_photo_alter_aboutme_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, related_name='images', to='article.photo'),
        ),
    ]
