# Generated by Django 4.2.6 on 2023-12-05 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0008_rename_funcao_perfil_atribuicao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('data_hora', models.DateTimeField(auto_now_add=True)),
                ('enviou', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enviou', to=settings.AUTH_USER_MODEL)),
                ('recebeu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recebeu', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]