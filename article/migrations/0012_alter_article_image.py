# Generated by Django 5.0.2 on 2024-02-10 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, related_name='Articles', to='article.photo'),
        ),
    ]
