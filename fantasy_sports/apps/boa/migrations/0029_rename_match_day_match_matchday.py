# Generated by Django 4.0.1 on 2022-02-08 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0028_rename_match_day_lineup_matchday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='match_day',
            new_name='matchday',
        ),
    ]