# Generated by Django 4.0.1 on 2022-01-16 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0007_alter_player_aoe2net_alter_player_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='manager',
            field=models.ManyToManyField(null=True, to='boa.Manager'),
        ),
    ]
