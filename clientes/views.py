from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente
from django.contrib import auth
from django.contrib.auth.models import User
from clientes.models import Cliente
from datetime import datetime


def logout(request):
    auth.logout(request)
    return redirect('index')


def login(request):
    nome = str(datetime.now().microsecond)
    senha = "123"
    user = User.objects.create_user(username=nome, password=senha)
    user.save()
    cliente, status = Cliente.objects.get_or_create(user=user)
    cliente.save()
    user = auth.authenticate(request, username=nome, password=senha)
    auth.login(request, user)
    return redirect(request.GET['next'])


def relog(request):
    auth.login(request, request.user)


