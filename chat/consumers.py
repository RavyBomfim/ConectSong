import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import Q
from usuarios.models import Mensagem

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Conexão WebSocket aberta.")

        # Recupera mensagens antigas e envia para o cliente
        user = self.scope['user']
        recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        messages = Mensagem.objects.filter(
            (Q(enviou=user, recebeu_id=recipient_id) | Q(enviou_id=recipient_id, recebeu=user))
        )
        for message in messages:
            await self.send(text_data=self.serialize_message(message))

    async def disconnect(self, close_code):
        print(f"Conexão WebSocket fechada. Código: {close_code}")

    async def receive(self, text_data):
        print(f"Mensagem recebida: {text_data}")
        
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        recipient_id = text_data_json.get('receive')  # Obtém o ID do destinatário

        # Verifica se o ID do destinatário é válido
        if not recipient_id:
            return

        # Obtém o usuário destinatário
        recipient_user = User.objects.get(pk=recipient_id)

        # Cria uma instância do modelo Mensagem e salva no banco de dados
        mensagem = Mensagem.objects.create(
            enviou=self.scope['user'],
            recebeu=recipient_user,
            mensagem=message_text
        )

        # Envia a mensagem de volta para o cliente
        await self.send(text_data=self.serialize_message(mensagem))

        # Atualiza a outra parte da conversa (WebSocket Group)
        await self.send_chat_message(recipient_id, mensagem)

    async def send_chat_message(self, recipient_id, message):
        # Construa um nome exclusivo para o grupo (usando IDs de usuários, por exemplo)
        room_name = f"user_{recipient_id}"

        # Adiciona o consumidor ao grupo (WebSocket Group)
        await self.channel_layer.group_add(
            room_name,
            self.channel_name
        )

        # Envia a mensagem para o grupo (WebSocket Group)
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat.message',
                'message': self.serialize_message(message)
            }
        )

    async def chat_message(self, event):
        # Envia a mensagem de volta para o cliente quando recebida do grupo (WebSocket Group)
        message = event['message']
        await self.send(text_data=message)

    def serialize_message(self, message):
        return json.dumps({
            'message': message.mensagem,
            'enviou_id': message.enviou.id,
            'recebeu_id': message.recebeu.id,
            'enviou_nome': message.enviou.perfil.nome_completo,
            'recebeu_nome': message.recebeu.perfil.nome_completo,
            'enviou_foto': str(message.enviou.perfil.foto_perfil.url) if message.enviou.perfil.foto_perfil else None,
            'recebeu_foto': str(message.recebeu.perfil.foto_perfil.url) if message.recebeu.perfil.foto_perfil else None,
            'data': message.data_hora.strftime("%Y-%m-%d"),
            'hora': message.data_hora.strftime("%H:%M:%S"),
        })


