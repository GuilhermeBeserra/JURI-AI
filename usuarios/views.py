from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from .models import Cliente
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senha e confirmar senha não são iguais.')
            return redirect('cadastro')
            
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'Sua senha deve ter pelo meno 6 caracteres.')
            return redirect('cadastro')

        users = User.objects.filter(username=username)
        
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse username.')
            return redirect('cadastro')
        
        User.objects.create_user(
            username=username,
            password=senha
        )

        return redirect('login')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(username=username, password=senha)
        if user is not None:
            auth.login(request, user)
            return redirect('clientes')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos.')
            return redirect('login')


@login_required
def clientes(request):
    if request.method == 'GET':
        clientes = Cliente.objects.filter(user=request.user)
        return render(request, 'clientes.html', {'clientes': clientes})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        tipo = request.POST.get('tipo')
        status = request.POST.get('status') == 'on'
        
        Cliente.objects.create(
            nome=nome,
            email=email,
            tipo=tipo,
            status=status,
            user=request.user
        )
        
        messages.add_message(request, constants.SUCCESS, 'Cliente cadastrado com sucesso!')
        return redirect('clientes')

from .models import Cliente, Documentos
def cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'GET':
        documentos = Documentos.objects.filter(cliente=cliente)
        return render(request, 'cliente.html', {'cliente': cliente, 'documentos': documentos})
    elif request.method == 'POST':
        tipo = request.POST.get('tipo')
        documento = request.FILES.get('documento')
        data = request.POST.get('data')
        
        documentos = Documentos(
            cliente=cliente,
            tipo=tipo,
            arquivo=documento,
            data_upload=data
        )
        documentos.save()

        return redirect(reverse('cliente', kwargs={'id': cliente.id}))