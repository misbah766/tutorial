# Generated by Django 3.2.7 on 2021-12-21 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drftask', '0015_alter_order_total_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='grand_total',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_quantity',
            field=models.IntegerField(),
        ),
    ]
