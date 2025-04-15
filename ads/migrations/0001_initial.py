# Generated by Django 5.1.4 on 2025-04-14 11:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='ads/%Y/%m/%d', verbose_name='Фото')),
                ('category', models.CharField(blank=True, max_length=100, null=True, verbose_name='Категория')),
                ('condition', models.CharField(choices=[('new', 'Новая'), ('like_new', 'Почти как новая'), ('used', 'Б/у'), ('poor', 'Сильно поношенная'), ('broken', 'Сломанная (на запчасти)')], max_length=15, verbose_name='Состояние')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
    ]
