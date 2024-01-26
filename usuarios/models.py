from django.db import models
from django.contrib.auth.models import User


sexo_opcoes = (('M', 'Masculino'), ('F', 'Feminino'), ('P', 'Prefiro não dizer'))

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    foto_capa = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    nome_completo = models.CharField(max_length=100, null=True, blank=True)
    atribuicao = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.TextField(blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=sexo_opcoes, null=True, blank=True) 
    cidade = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.nome_completo}'

    def get_atribuicao_display(self):
        return self.atribuicao.split('/') if self.atribuicao else []
    

class Conexao(models.Model):
    enviou_solicitacao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conexao_enviada')
    recebeu_solicitacao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conexao_recebida')
    status = models.BooleanField(default=False)


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


class Mensagem(models.Model):
    enviou = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enviou')
    recebeu = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recebeu')
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
