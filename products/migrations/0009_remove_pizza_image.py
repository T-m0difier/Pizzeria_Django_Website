# Generated by Django 5.1.3 on 2024-12-08 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_cartitem_pizza_name_alter_crust_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='image',
        ),
    ]