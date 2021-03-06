# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 16:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_belt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('startdate', models.DateTimeField()),
                ('enddate', models.DateTimeField()),
                ('plan', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TripDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tripplan', to='django_belt.Trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tripuser', to='django_belt.User')),
                ('users', models.ManyToManyField(related_name='tripusers', to='django_belt.Trip')),
            ],
        ),
    ]
