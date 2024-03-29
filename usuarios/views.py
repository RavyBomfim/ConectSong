from django.conf import settings
from django.db.models import  Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from usuarios.models import Perfil, Conexao, Post, Imagem, Video
from django.views.generic import TemplateView
from .forms import CustomAuthenticationForm, PerfilForm
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PublicacaoForm


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = CustomAuthenticationForm

class VerPerfil(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'usuarios/perfil.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        perfil = Perfil.objects.get(usuario=user.id) 

        conexao = Conexao.objects.filter(
            (Q(enviou_solicitacao=self.request.user) & Q(recebeu_solicitacao=perfil.usuario)) |
            (Q(enviou_solicitacao=perfil.usuario) & Q(recebeu_solicitacao=self.request.user))
        ).first()

        conexoes = Conexao.objects.filter((Q(enviou_solicitacao=perfil.usuario) | Q(recebeu_solicitacao=perfil.usuario)) & Q(status=True))[:6]

        connections = []

        for connect in conexoes: 
            if connect.enviou_solicitacao != perfil.usuario:
                connection = connect.enviou_solicitacao
            else:
                connection = connect.recebeu_solicitacao

            connections.append(connection.perfil)

        context['perfil'] = perfil
        context['conexao'] = conexao
        context['posts'] = Post.objects.filter(usuario=user)
        context['connections'] = connections
        context['qtd_connections'] = conexoes.count()
        
        return context
    

class PerfilUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = 'usuarios/form_perfil.html'
    model = Perfil
    form_class = PerfilForm

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user.perfil
        return None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['atribuicao'].initial = [opcao[0:] for opcao in form.instance.get_atribuicao_display()]
        return form

    def form_valid(self, form):
        atribuicao_selecionada = [item[0:] for item in form.cleaned_data['atribuicao']]
        sexo = form.cleaned_data['sexo']
        atribuicao_ajustada = atribuicao_selecionada

        if sexo == 'F':
            atribuicao_ajustada = [opcao + 'a' for opcao in atribuicao_selecionada]
        elif sexo == 'P' or sexo == '':
            atribuicao_ajustada = [opcao + '(a)' for opcao in atribuicao_selecionada]
        
        form.instance.atribuicao = '/'.join(atribuicao_ajustada)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        user = self.request.user
        perfil = Perfil.objects.get(usuario=user)

        foto = {
            'foto': perfil.foto_perfil if perfil.foto_perfil else '',
        }
        context['foto'] = foto

        return context

    def get_success_url(self):
        username = self.request.user.username
        success_url = reverse('ver-perfil', kwargs={'username': username})
        return success_url
        

@login_required
def criar_publicacao(request):
    if request.method == 'POST':
        form = PublicacaoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.usuario = request.user  
            post.save()

            imagem = form.cleaned_data.get('imagem')
            if imagem:
                Imagem.objects.create(post=post, imagem=imagem)

            video = form.cleaned_data.get('video')
            if video:
                Video.objects.create(post=post, video=video)

            # Redirecionar de volta para a página anterior
            return redirect(request.META.get('HTTP_REFERER', 'inicio'))
    else:
        form = PublicacaoForm()

    return render(request, 'paginas/index.html', {'form': form})


'''def editar_publicacao(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        form = PublicacaoForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.usuario = request.user  
            post.save()

            imagem = form.cleaned_data.get('imagem')
            if imagem:
                Imagem.objects.create(post=post, imagem=imagem)

            video = form.cleaned_data.get('video')
            if video:
                Video.objects.create(post=post, video=video)

            # Redirecionar de volta para a página anterior
            return redirect(request.META.get('HTTP_REFERER', 'inicio'))

    return render(request, 'paginas/index.html', {'form': form, 'post': post})'''


@login_required
def alterar_foto_capa(request):
    if request.method == 'POST':
        id_perfil = request.POST.get('id-perfil')
        nova_foto_capa = request.FILES.get('foto-capa')
        perfil = get_object_or_404(Perfil, pk=id_perfil)

        if nova_foto_capa:
            perfil.foto_capa = nova_foto_capa
            perfil.save()
    return voltar_para_pagina_anterior(request)


def alterar_foto_perfil(request):
    if request.method == 'POST':
        id_perfil = request.POST.get('id-perfil')
        nova_foto_perfil = request.FILES.get('foto-perfil')
        perfil = get_object_or_404(Perfil, pk=id_perfil)

        if nova_foto_perfil:
            perfil.foto_perfil = nova_foto_perfil
            perfil.save()
    return voltar_para_pagina_anterior(request) 


class PerfisResultados(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Perfil
    template_name = 'usuarios/lista/resultados_pesquisa.html'

    def get_queryset(self):

        caracteres = self.request.GET.get('search')

        perfis = Perfil.objects.filter(
            Q(nome_completo__istartswith=caracteres) |
            Q(nome_completo__icontains=f' {caracteres}')
        ).order_by('-nome_completo')

        user_in_list = any(perfil.usuario == self.request.user for perfil in perfis)

        if user_in_list:
            perfis = sorted(perfis, key=lambda p: p.usuario != self.request.user, reverse=True)


        conexoes = Conexao.objects.filter(Q(enviou_solicitacao=self.request.user) | Q(recebeu_solicitacao=self.request.user))

        for perfil in perfis:
            perfil.conexao = self.get_connection(conexoes, perfil)

        return perfis

    def get_connection(self, conexoes, perfil):
        for conexao in conexoes:
            if conexao.enviou_solicitacao == perfil.usuario or conexao.recebeu_solicitacao == perfil.usuario:
                return conexao
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conexoes'] = self.get_connections(self.object_list)
        return context

    def get_connections(self, perfis):
        return [perfil.conexao for perfil in perfis]


@login_required
def pesquisar_perfis(request): 
    if request.method == 'GET':
        caracteres = request.GET.get('search')

        perfis = Perfil.objects.filter(
            Q(nome_completo__istartswith=caracteres) |
            Q(nome_completo__icontains=f' {caracteres}')
        ).order_by('-nome_completo')[:8]


        perfis_lista = []
        for perfil in perfis:
            perfil_data = {
                'perfil_username': perfil.usuario.username,
                'nome_completo': perfil.nome_completo,
                'foto_perfil': perfil.foto_perfil.url if perfil.foto_perfil else None,
                'atribuicao': perfil.atribuicao
            }
            perfis_lista.append(perfil_data)

        return JsonResponse({'perfis': perfis_lista})
    else:
        return JsonResponse({'erro': 'Apenas métodos GET são permitidos'})


def voltar_para_pagina_anterior(request):
    url_anterior = request.META.get('HTTP_REFERER', reverse('inicio'))
    return redirect(url_anterior)


@login_required
def solicitar_conexao(request):
    recebeu_solicitacao = request.POST.get('recebeu-solicitacao')
    conectar_a_usuario = get_object_or_404(User, id=recebeu_solicitacao)

    if not Conexao.objects.filter(enviou_solicitacao=request.user, recebeu_solicitacao=conectar_a_usuario).exists():
        Conexao.objects.create(enviou_solicitacao=request.user, recebeu_solicitacao=conectar_a_usuario)

    return voltar_para_pagina_anterior(request)    


@login_required
def aceitar_conexao(request):
    if request.method == 'POST':
        conexao_id = request.POST.get('conexao-id')
        conexao = get_object_or_404(Conexao, id=conexao_id)

        if request.user == conexao.recebeu_solicitacao:
            conexao.status = True
            conexao.save()

    return voltar_para_pagina_anterior(request)
    

@login_required
def cancelar_solicitacao(request):
    if request.method == 'POST':
        conexao_id = request.POST.get('conexao_id')
        conexao = get_object_or_404(Conexao, id=conexao_id)

        if request.user == conexao.enviou_solicitacao:
            conexao.delete()

    return voltar_para_pagina_anterior(request)



'''@login_required
def enviar_mensagem(request):
    if request.method == 'POST':
        mensagem = request.POST.get('message')
        enviou = request.user
        recebeu = request.POST.get('receive')
        conexao = get_object_or_404(Conexao, id=conexao_id)

        if request.user == conexao.enviou_solicitacao:
            conexao.delete()

    return voltar_para_pagina_anterior(request)
'''
