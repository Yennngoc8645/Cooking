# Generated by Django 5.1.1 on 2025-01-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dopamine', '0003_product_image_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
    ]
