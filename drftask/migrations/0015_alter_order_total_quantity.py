# Generated by Django 3.2.7 on 2021-12-21 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drftask', '0014_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_quantity',
            field=models.IntegerField(max_length=200),
        ),
    ]
