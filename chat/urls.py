from django.urls import path
from .views import carregar_mensagens, enviar_mensagem

urlpatterns = [
    path('carregar-mensagens/<int:user_id>/', carregar_mensagens, name='carregar_mensagens'),
    path('enviar-mensagem', enviar_mensagem, name='enviar_mensagem'),
    # ... outras URLs do seu aplicativo ...
]
