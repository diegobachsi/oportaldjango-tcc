from django.db import models

class Contato(models.Model):

    nome = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    email = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    message = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    objetos = models.Manager()
