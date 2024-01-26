from django.urls import path
from django.contrib.auth import views as auth_views
from usuarios.views import CustomLoginView, PerfilUpdate, PerfisResultados, VerPerfil, aceitar_conexao, alterar_foto_capa, alterar_foto_perfil, cancelar_solicitacao, criar_publicacao, pesquisar_perfis, solicitar_conexao
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuarios/login.html'
    ), name='logout'),
    path('perfil/editar', PerfilUpdate.as_view(), name='editar-perfil'),
    path('perfil/<str:username>', VerPerfil.as_view(), name='ver-perfil'),
    path('perfil/editar/capa', alterar_foto_capa, name='editar-capa'),
    path('perfil/editar/foto-perfil', alterar_foto_perfil, name='editar-foto-perfil'),
    path('pesquisar/perfis/', pesquisar_perfis, name='pesquisar-perfis'),
    path('perfis/resultados', PerfisResultados.as_view(), name='perfis-resultados'),

    path('solicitar/conexao', solicitar_conexao, name='enviar-solicitacao'),
    path('solicitacao/conexao/aceitar', aceitar_conexao, name='aceitar-solicitacao'),
    path('cancelar-solicitacao/', cancelar_solicitacao, name='cancelar-solicitacao'),
    path('criar/publicacao/', criar_publicacao, name='criar-publicacao'),
]