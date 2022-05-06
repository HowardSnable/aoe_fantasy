# Generated by Django 4.0.1 on 2022-02-09 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boa', '0029_rename_match_day_match_matchday'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_alive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='l1',
            field=models.ForeignKey(limit_choices_to={'team.is_alive': True}, on_delete=django.db.models.deletion.CASCADE, related_name='l1', to='boa.player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='l2',
            field=models.ForeignKey(limit_choices_to={'team.is_alive': True}, on_delete=django.db.models.deletion.CASCADE, related_name='l2', to='boa.player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='l3',
            field=models.ForeignKey(limit_choices_to={'team.is_alive': True}, on_delete=django.db.models.deletion.CASCADE, related_name='l3', to='boa.player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='mvp1',
            field=models.ForeignKey(limit_choices_to={'team.is_alive': True}, on_delete=django.db.models.deletion.CASCADE, related_name='mvp1', to='boa.player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='mvp2',
            field=models.ForeignKey(limit_choices_to={'team.is_alive': True}, on_delete=django.db.models.deletion.CASCADE, related_name='mvp2', to='boa.player'),
        ),
    ]
