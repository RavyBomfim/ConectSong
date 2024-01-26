import json
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from usuarios.models import Mensagem
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User


@login_required
def carregar_mensagens(request, user_id):
    
    mensagens = Mensagem.objects.filter(
        (Q(enviou=request.user, recebeu=user_id) | Q(enviou=user_id, recebeu=request.user))
    ).order_by('data_hora')

    mensagens_data = []
    for mensagem in mensagens:
        mensagem_data = {
            'message': mensagem.mensagem,
            'enviou_id': mensagem.enviou.id,
            'recebeu_id': mensagem.recebeu.id,
            'enviou_nome': mensagem.enviou.perfil.nome_completo,
            'recebeu_nome': mensagem.recebeu.perfil.nome_completo,
            'enviou_foto': str(mensagem.enviou.perfil.foto_perfil.url) if mensagem.enviou.perfil.foto_perfil else None,
            'recebeu_foto': str(mensagem.recebeu.perfil.foto_perfil.url) if mensagem.recebeu.perfil.foto_perfil else None,
            'data': mensagem.data_hora.strftime("%Y-%m-%d"),
            'hora': mensagem.data_hora.strftime("%H:%M"),
        }
        mensagens_data.append(mensagem_data)

    return JsonResponse({'mensagens': mensagens_data})


@login_required
def enviar_mensagem(request):
    try:
        # Obtenha os dados do corpo da requisição
        data = json.loads(request.body.decode('utf-8'))

        # Extraia os dados necessários
        mensagem = data.get('message')
        recebeu_id = data.get('receive')
        recebeu = get_object_or_404(User, id=recebeu_id)

        # Crie uma nova instância de Mensagem e salve-a no banco de dados
        nova_mensagem = Mensagem.objects.create(
            enviou=request.user,
            recebeu=recebeu,
            mensagem=mensagem
        )

        nova_mensagem.save()

        # Retorne uma resposta de sucesso
        return JsonResponse({'status': 'success'})

    except Exception as e:
        # Em caso de erro, retorne uma resposta de erro com uma mensagem apropriada
        return JsonResponse({'status': 'error', 'message': str(e)})
