from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.


def cadastro(request):
    # Fazemos algumas validações na view para que as infromações do usuario estejam corretas
    if request.method == 'POST':
        # 'nome' é o nome que foi dado no form do html
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if not nome.strip():
            print('O campo nome não pode ficar em branco')
            return redirect('cadastro')
        if not nome.strip():
            print('O campo senha não pode ficar em branco')
            return redirect('cadastro')
        if senha != senha2:
            print('As senhas não coincidem')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            print('Usuario já cadastrado')
            return redirect('cadastro')

        # Caso estejam ok, criamos e salvamos o usuario no banco
        user = User.objects.create_user(
            username=nome, email=email, password=senha)
        user.save()

        print('Usuario cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    return render(request, 'usuarios/login.html')


def dashboard(request):
    pass


def logout(request):
    pass
