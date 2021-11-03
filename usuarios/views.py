from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from receitas.models import Receita
# Create your views here.


def cadastro(request):
    # Fazemos algumas validações na view para que as infromações do usuario estejam corretas
    if request.method == 'POST':
        # 'nome' vindo da tag name do cadastro.html
        nome = request.POST['nome']
        # 'email' vindo da tag name do cadastro.html
        email = request.POST['email']
        # 'senha' vindo da tag name do cadastro.html
        senha = request.POST['password']
        # 'senha' vindo da tag name do cadastro.html
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
        # 'email' vindo da tag name do login.html
        email = request.POST['email']
        # 'senha' vindo da tag name do login.html
        senha = request.POST['senha']

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
        # Criando receitas de acordo com o id do usuario
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

        # Criando dicionario de dados a partir das receitas
        dados = {
            'receitas': receitas
        }

        # Renderizando pagina de dashboard com as receitas do usuario
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def logout(request):
    # Realizando logout do usuario e redirecionando ao index
    auth.logout(request)
    return redirect('index')


def cria_receita(request):
    if request.method == "POST":
        # 'nome_receita'  vindo da tag name do cria_receita.html
        nome_receita = request.POST['nome_receita']
        # 'ingredientes'  vindo da tag name do cria_receita.html
        ingredientes = request.POST['ingredientes']
        # 'modo_preparo'  vindo da tag name do cria_receita.html
        modo_preparo = request.POST['modo_preparo']
        # 'tempo_preparo' vindo da tag name do cria_receita.html
        tempo_preparo = request.POST['tempo_preparo']
        # 'rendimento'    vindo da tag name do cria_receita.html
        rendimento = request.POST['rendimento']
        # 'categoria'     vindo da tag name do cria_receita.html
        categoria = request.POST['categoria']
        # 'foto_receita'  vindo da tag name do cria_receita.html -> FILES -- Para trazer o arquivo da foto
        foto_receita = request.FILES['foto_receita']

        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(
            pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)

        receita.save()

        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html  ')
