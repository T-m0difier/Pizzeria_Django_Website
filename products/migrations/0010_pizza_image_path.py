# Generated by Django 5.1.3 on 2024-12-11 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_pizza_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='image_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
