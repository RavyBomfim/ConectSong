from typing import Any
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from usuarios.models import Post, Imagem, Video
from usuarios.views import voltar_para_pagina_anterior

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'paginas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context
    

@login_required
def excluir_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        if request.user == post.usuario:
            post.delete()

    return voltar_para_pagina_anterior(request)


@receiver(pre_delete, sender=Post)
def deletar_videos_e_fotos_relacionados(sender, instance, **kwargs):
    imagens_relacionadas = Imagem.objects.filter(post=instance)
    for imagem in imagens_relacionadas:
        imagem.imagem.delete()
        imagem.delete()

    videos_relacionados = Video.objects.filter(post=instance)
    for video in videos_relacionados:
        video.video.delete()
        video.delete()
    