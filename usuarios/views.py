from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
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
        if not email.strip():
            print('O campo email não pode ficar em branco')
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
    # Realizando validações
    if request.method == 'POST':
        email = request.POST['email']  # 'email' vindo da tag name do html
        senha = request.POST['senha']  # 'senha' vindo da tag name do html

        # Verificando se o email e senha estão preenchidos, caso não estejam a pagina será recarregada
        if email.strip() == '' or senha == '':
            print('Os campos email e senha não podem ficar em branco')
            return redirect('login')

        # Django uttiliza no sistema de autenticação o usuario e a senha, então precisamos pegar o usuario pelo email.
        # Verificamos se o email existe no banco de dados.
        if User.objects.filter(email=email).exists():
            # Atribuindo na variavel nome o username do usuario, que foi pego atravéz do email
            nome = User.objects.filter(email=email).values_list(
                'username', flat=True).get()

            # Atribuindo na variavel user o valor do usuario e a senha
            user = auth.authenticate(request, username=nome, password=senha)
            # Se o user estiver preechido corretamente, iremos logar corretamente
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('dashboard')

    return render(request, 'usuarios/login.html')


def dashboard(request):
    # Se o usuario estiver logado ele consegue ver a pagina de dashboard, caso contrario ele será redirecionado para a index
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect('index')


def logout(request):
    # Realizando logout do usuario e redirecionando ao index
    auth.logout(request)
    return redirect('index')
