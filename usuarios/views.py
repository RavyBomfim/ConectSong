from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from usuarios.models import Perfil
from django.views.generic import TemplateView
from .forms import CustomAuthenticationForm, PerfilForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = CustomAuthenticationForm

class VerPerfil(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'usuarios/perfil.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        perfil = Perfil.objects.get(id=user.id) 
        context['perfil'] = perfil
        return context
    

class PerfilUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = 'usuarios/form-perfil.html'
    model = Perfil
    form_class = PerfilForm
    success_url = reverse_lazy('perfil')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        perfil = self.object

        foto = {
            'foto_perfil': perfil.foto_perfil if perfil.foto_perfil else '',
        }
        context['foto'] = foto

        return context