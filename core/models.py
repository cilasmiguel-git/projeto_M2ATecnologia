from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    NIVEIS_ACESSO = [
        ('comum', 'Comum'),
        ('admin', 'Administrador')
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nivel_acesso = models.CharField(max_length=10, choices=NIVEIS_ACESSO, default='comum')

    def set_senha(self, senha):
        self.senha = make_password(senha)
        self.save()

    def check_senha(self, senha):
        return check_password(senha, self.senha)

    def __str__(self):
        return self.nome
class Ponto(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    entrada = models.TimeField()
    saida = models.TimeField(null=True, blank=True)

    @property
    def horas_trabalhadas(self):
        if self.saida:
            entrada_datetime = datetime.combine(self.data, self.entrada)
            saida_datetime = datetime.combine(self.data, self.saida)
            return (saida_datetime - entrada_datetime).total_seconds() / 3600
        return 0
