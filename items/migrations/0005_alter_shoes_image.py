# Generated by Django 5.0.7 on 2024-08-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_alter_shoes_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoes',
            name='image',
            field=models.ImageField(default='', upload_to='shoes/items/images'),
        ),
    ]
