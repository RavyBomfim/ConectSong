from django import forms
from django.contrib.auth.forms import AuthenticationForm
from usuarios.models import Perfil, Post, sexo_opcoes

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput)
    error_messages = {
        'invalid_login': 'Email ou senha inválidos!',
    }


class PerfilForm(forms.ModelForm):
    atribuicao_opcoes = (('Cantor', 'Cantor'), ('Compositor', 'Compositor'), ('Produtor', 'Produtor'))

    atribuicao = forms.MultipleChoiceField(
        choices=(atribuicao_opcoes),  # Substitua com suas opções
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'atribuicao-checkbox'}),
    )
    sexo = forms.ChoiceField(choices=(sexo_opcoes), initial=None)

    class Meta:
        model = Perfil
        fields = ['nome_completo', 'foto_perfil', 'atribuicao', 'descricao', 'data_nascimento', 'cidade', 'sexo']
        widgets = {
            'foto_perfil' :forms.ClearableFileInput(attrs={'class': 'foto'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['atribuicao'].choices = self.atribuicao_opcoes

        atribuicao_atual = self.instance.atribuicao.split('/') if self.instance.atribuicao else []
        self.fields['atribuicao'].initial = atribuicao_atual


class PublicacaoForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite seu texto aqui...'}), required=False)
    imagem = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['texto', 'imagem', 'video']

    '''def save(self, commit=True):
        if not (self.cleaned_data['texto'] or self.cleaned_data['imagem'] or self.cleaned_data['video']):
            return super().save(commit=False)  # Retorna a instância sem salvar no banco de dados
        return super().save(commit)'''
