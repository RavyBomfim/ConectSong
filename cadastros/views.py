from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from cadastros.forms import UsuarioForm

# Create your views here.
class UsuarioCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = UsuarioForm
    template_name = 'cadastros/form_usuario.html'
    success_url = reverse_lazy('login')

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de Novo Usuário'

        return context