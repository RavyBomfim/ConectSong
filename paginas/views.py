from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from usuarios.models import Perfil

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'paginas/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        perfil = Perfil.objects.get(usuario=user.id)
        context['perfil'] = perfil
        return context
    
    
    