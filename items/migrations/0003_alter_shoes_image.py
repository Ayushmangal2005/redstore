# Generated by Django 5.0.7 on 2024-08-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_rename_tiles_shoes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoes',
            name='image',
            field=models.ImageField(default='', upload_to='static/images'),
        ),
    ]
