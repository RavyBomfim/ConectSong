# Generated by Django 4.2.6 on 2023-11-01 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_rename_foto_perfil_foto_perfil_perfil_foto_capa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='nome_completo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
