from django.contrib.auth.models import User
from django.db import models


class Cliente(models.Model):
    TIPO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='PF')
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

from martor.models import MartorField
class Documentos(models.Model):
    TIPO_CHOICES = [
        ('C', 'Contrato'),
        ('P', 'Petição'),
        ('CONT', 'Contestação'),
        ('R', 'Recursos'),
        ('O', 'Outro'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES, default='O')
    arquivo = models.FileField(upload_to='documentos/')
    data_upload = models.DateTimeField()
    content = MartorField()

    def __str__(self):
        return self.tipo