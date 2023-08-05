# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-24 19:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='sent at')),
                ('read_at', models.DateTimeField(blank=True, null=True, verbose_name='read at')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_dm', to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_dm', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
        ),
    ]
