from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from cadastros.forms import UsuarioForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from usuarios.models import Perfil

# Create your views here.
class UsuarioCreate(CreateView):
    form_class = UsuarioForm
    template_name = 'cadastros/form_usuario.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.username = form.cleaned_data.get('email').split('@')[0]
        form_data = {'nome_completo': form.cleaned_data.get('nome_completo')}
        form.instance.form_data = form_data
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Cadastro de Novo Usuário'
        return context


@receiver(post_save, sender=User)
def criar_perfil_de_usuario(sender, instance, created, **kwargs):
    if created:
        form_data = getattr(instance, 'form_data', None)
        nome_completo = form_data.get('nome_completo') if form_data else None
        Perfil.objects.create(usuario=instance, nome_completo=nome_completo)