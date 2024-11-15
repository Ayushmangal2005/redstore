from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_is_actice_cartitem_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
