from django.urls import path
from cadastros.views import UsuarioCreate

urlpatterns = [
    path('cadastrar/usuario', UsuarioCreate.as_view(), name='cadastrar-usuario'),
]