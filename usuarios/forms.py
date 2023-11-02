from django import forms
from django.contrib.auth.forms import AuthenticationForm

from usuarios.models import Perfil

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Usuário ou senha inválidos!',
    }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome_completo', 'foto_perfil', 'descricao', 'data_nascimento', 'cidade', 'telefone']
        widgets = {
            'foto_perfil' :forms.ClearableFileInput(attrs={'class': 'foto'})
        }