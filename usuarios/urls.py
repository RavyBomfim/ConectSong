from django.urls import path
from django.contrib.auth import views as auth_views
from usuarios.views import CustomLoginView, PerfilUpdate, VerPerfil

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuarios/login.html'
    ), name='logout'),
    path('usuario/perfil', VerPerfil.as_view(), name='perfil'),
    path('usuario/perfil/editar/<int:pk>', PerfilUpdate.as_view(), name='editar-perfil'),
]