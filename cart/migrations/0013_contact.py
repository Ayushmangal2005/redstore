# Generated by Django 5.0.7 on 2024-11-14 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_cartitem_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
            ],
        ),
    ]
