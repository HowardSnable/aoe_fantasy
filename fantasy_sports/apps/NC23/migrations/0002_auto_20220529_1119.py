# Generated by Django 2.1 on 2022-05-29 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='aoe2net',
        ),
        migrations.RemoveField(
            model_name='player',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='player',
            name='image',
        ),
        migrations.AlterField(
            model_name='player',
            name='def_price',
            field=models.IntegerField(default=100),
        ),
    ]
