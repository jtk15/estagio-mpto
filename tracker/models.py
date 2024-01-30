from django.db import models


class State(models.Model):
    name = models.CharField('Nome', max_length=30, unique=True)
    abreviattion = models.CharField('Sigla', max_length=2, unique=True)
