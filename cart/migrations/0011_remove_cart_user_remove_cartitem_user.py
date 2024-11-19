from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_alter_cart_cart_id_alter_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
    ]