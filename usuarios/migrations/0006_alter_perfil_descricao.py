# Generated by Django 4.2.6 on 2023-12-02 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_alter_perfil_nome_completo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='descricao',
            field=models.TextField(blank=True),
        ),
    ]
