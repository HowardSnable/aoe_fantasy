# Generated by Django 4.0.1 on 2022-02-08 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0027_remove_lineup_id_result_points_alter_lineup_manager'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineup',
            old_name='match_day',
            new_name='matchday',
        ),
    ]