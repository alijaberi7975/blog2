# Generated by Django 5.0.2 on 2024-02-17 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0028_alter_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='Articles', to='article.category'),
        ),
    ]
