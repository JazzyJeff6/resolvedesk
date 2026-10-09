from django.db import models
from django.conf import settings

# Create your models here.

from django.db import models


class Chamado(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em andamento'),
        ('resolvido', 'Resolvido'),
    ]

    solucao = models.TextField(blank=True, default='')
    
    
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto',
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='chamados',
        null=True,
        blank=True,
    )