from django.contrib.auth.models import User
from django.db import models


class AbstractLeague(models.Model):
    name = models.CharField(max_length=50, unique=True)
    administrator = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.name)


class AbstractTeam(models.Model):
    name = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} - {}'.format(self.name, self.owner)


class AbstractPlayer(models.Model):
    first_name = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=30, unique=True)
    date_of_birth = models.DateField()
    is_injured = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class AbstractTournament(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    draw_size = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.name)
