# Generated by Django 3.2.6 on 2022-01-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20220102_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerForum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100, verbose_name='Usuário')),
                ('id_topico_forum', models.CharField(max_length=255, verbose_name='Tópico Fórum')),
                ('answer', models.TextField(blank=True, verbose_name='Resposta')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em:')),
            ],
        ),
    ]
