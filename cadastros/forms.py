import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UsuarioForm(UserCreationForm):
    nome_completo = forms.CharField(max_length=255)
    username = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=100) 

    class Meta:
        model = User
        fields = ['nome_completo', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já possui uma conta cadastrada.')
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError('A senha deve ter pelo menos 8 caracteres.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('A senha deve conter pelo menos um número.')
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra.')
        # if not any(char.isalpha() for char in password1) or not re.search("[!@#$%^&*(),.?\":{}|<>]", password1): 
        #     raise forms.ValidationError('A senha deve conter pelo menos uma letra e um caractere especial.')
        return password1

    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('*As senhas não coincidem.')

        return password2