# Generated by Django 3.2.7 on 2021-12-20 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drftask', '0007_favourite_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='favorite',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
