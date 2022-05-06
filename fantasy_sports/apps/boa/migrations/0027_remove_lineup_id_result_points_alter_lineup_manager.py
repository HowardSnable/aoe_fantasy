# Generated by Django 4.0.1 on 2022-02-06 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0026_result_delete_lineupadapter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineup',
            name='id',
        ),
        migrations.AddField(
            model_name='result',
            name='points',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lineup',
            name='manager',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='lineup_manager', serialize=False, to='boa.manager'),
        ),
    ]
