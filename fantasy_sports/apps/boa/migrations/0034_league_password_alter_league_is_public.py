# Generated by Django 4.0.1 on 2022-03-26 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0033_result_games_flank'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='password',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='league',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]