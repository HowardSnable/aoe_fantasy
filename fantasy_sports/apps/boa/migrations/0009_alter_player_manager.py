# Generated by Django 4.0.1 on 2022-01-16 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0008_alter_player_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='manager',
            field=models.ManyToManyField(blank=True, to='boa.Manager'),
        ),
    ]