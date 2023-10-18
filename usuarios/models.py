from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cidade = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)


class Post(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(null=True, blank=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_publicacao']


class Imagem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='post_images/')


class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.FileField(upload_to='post_videos/')
