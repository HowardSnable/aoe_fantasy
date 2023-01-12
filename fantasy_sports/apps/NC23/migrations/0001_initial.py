# Generated by Django 2.1 on 2023-01-12 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('is_public', models.BooleanField(default=False)),
                ('max_teams_per_league', models.PositiveIntegerField(default=10)),
                ('max_players_per_team', models.PositiveIntegerField(default=4)),
                ('points_per_match_win', models.FloatField(default=1)),
                ('points_per_match_loss', models.FloatField(default=-0.5)),
                ('point_for_mvp', models.FloatField(default=0.3)),
                ('captain_factor', models.FloatField(default=2.0)),
                ('points_for_position', models.FloatField(default=0.2)),
                ('transfers_per_day', models.IntegerField(default=6)),
                ('password', models.CharField(blank=True, max_length=50)),
                ('administrator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nc23_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('points', models.FloatField(default=0)),
                ('budget', models.IntegerField(default=2500)),
                ('icon', models.TextField(blank=True, default='')),
                ('name', models.CharField(default='Team', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.TextField(blank=True, null=True)),
                ('date_played', models.DateTimeField(default=None, null=True)),
                ('number_games', models.PositiveIntegerField(default=1)),
                ('winner', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MatchDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_round', models.CharField(choices=[('G1', 'Group stage round 1'), ('G2', 'Group stage round 2'), ('G3', 'Group stage round 3'), ('16', 'Round of 16'), ('8', 'Quarter-Finals'), ('4', 'Semi-Finals'), ('2', 'Finals')], max_length=10)),
                ('is_active', models.BooleanField(default=False)),
                ('is_booked', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(default=None, null=True)),
                ('end_date', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(default=None, null=True)),
                ('end_date', models.DateTimeField(default=None, null=True)),
                ('price', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nc23.League')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('liquipedia', models.TextField(blank=True, default='')),
                ('def_price', models.IntegerField(default=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField()),
                ('games_pocket', models.IntegerField(default=0)),
                ('games_flank', models.IntegerField(default=0)),
                ('matchday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_day', to='nc23.MatchDay')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_player', to='nc23.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liquipedia', models.TextField(blank=True, default='')),
                ('name', models.TextField(blank=True, default='')),
                ('long_name', models.TextField(blank=True, default='')),
                ('icon', models.TextField(blank=True, default='')),
                ('is_alive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransferMarket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(default=None, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('price', models.IntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tr_league', to='nc23.League')),
            ],
        ),
        migrations.CreateModel(
            name='LineUp',
            fields=[
                ('captain', models.IntegerField(default=0)),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='lineup_manager', serialize=False, to='nc23.Manager')),
            ],
        ),
        migrations.AddField(
            model_name='transfermarket',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tr_manager', to='nc23.Manager'),
        ),
        migrations.AddField(
            model_name='transfermarket',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tr_player', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='player',
            name='manager',
            field=models.ManyToManyField(blank=True, to='nc23.Manager'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='nc23.Team'),
        ),
        migrations.AddField(
            model_name='offer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='offer',
            name='reciever',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to='nc23.Manager'),
        ),
        migrations.AddField(
            model_name='offer',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='nc23.Manager'),
        ),
        migrations.AddField(
            model_name='match',
            name='matchday',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_day', to='nc23.MatchDay'),
        ),
        migrations.AddField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='nc23.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='nc23.Team'),
        ),
        migrations.AddField(
            model_name='manager',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nc23.League'),
        ),
        migrations.AddField(
            model_name='manager',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nc23_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='l1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l1', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='l2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l2', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='l3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l3', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='l4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l4', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match', to='nc23.Match'),
        ),
        migrations.AddField(
            model_name='game',
            name='mvp1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mvp1', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='mvp2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mvp2', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='w1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='w1', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='w2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='w2', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='w3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='w3', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='w4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='w4', to='nc23.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together={('team1', 'team2')},
        ),
        migrations.AddField(
            model_name='lineup',
            name='flank1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flank1', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='flank2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flank2', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='matchday',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='l_match_day', to='nc23.MatchDay'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='pocket1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pocket1', to='nc23.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='pocket2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pocket2', to='nc23.Player'),
        ),
    ]
