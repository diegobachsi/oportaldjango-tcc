# Generated by Django 3.2.6 on 2021-08-22 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
        ('videos', '0004_remove_videos_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='curso',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cursos.cursos'),
            preserve_default=False,
        ),
    ]
