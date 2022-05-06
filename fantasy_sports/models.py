from django.contrib.auth.models import User
from django.db import models


class AbstractLeague(models.Model):
    name = models.CharField(max_length=50, unique=True)
    administrator = models.ForeignKey(User, on_delete=models.PROTECT)
    date_created = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.name)


class AbstractManager(models.Model):
    name = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} - {}'.format(self.name, self.user)


class AbstractPlayer(models.Model):
    name = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

