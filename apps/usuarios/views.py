from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

# Create your views here.


def cadastro(request):
    """ Cadastra uma nova pessoa no sistema """
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

        if campo_vazio(nome):
            # implementando mensagens de erro
            messages.error(request, 'O campo nome não pode ficar em branco')
            dados = {
                'email': email,
                'senha': senha,
            }
            return render(request, 'usuarios/cadastro.html', dados)
            # return redirect('cadastro')

        if campo_vazio(email):
            return redirect('cadastro')

        if senhas_nao_sao_iguais(senha, senha2):
            # implementando mensagens de erro
            messages.error(request, 'As senhas não coincidem')

            dados = {
                'nome': nome,
                'email': email,
                'senha': senha,
            }
            return render(request, 'usuarios/cadastro.html', dados)
            # return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            # implementando mensagens de erro
            messages.error(request, 'Usuario já cadastrado')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            # implementando mensagens de erro
            messages.error(request, 'Usuario já cadastrado')
            return redirect('cadastro')

        # Caso estejam ok, criamos e salvamos o usuario no banco
        user = User.objects.create_user(
            username=nome, email=email, password=senha)
        user.save()

        # implementando mensagens de sucesso
        messages.success(request, 'Usuario cadastrado com sucesso!')
        return redirect('login')

    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """ Realiza um login de uma pessoa no sistema """
    # Realizando validações
    if request.method == 'POST':
        # 'email' vindo da tag name do login.html
        email = request.POST['email']
        # 'senha' vindo da tag name do login.html
        senha = request.POST['senha']

        # Verificando se o email e senha estão preenchidos, caso não estejam a pagina será recarregada
        if campo_vazio(email) or campo_vazio(senha):
            # implementando mensagens de erro
            messages.error(
                request, 'Os campos email ou senha não podem ficar em branco')
            return redirect('login')

        # Django uttiliza no sistema de autenticação o usuario e a senha, então precisamos pegar o usuario pelo email.
        # Verificamos se o email existe no banco de dados.
        if User.objects.filter(email=email).exists():
            # Atribuindo na variavel nome o username do usuario, que foi pego atravéz do email
            nome = User.objects.filter(email=email).values_list(
                'username', flat=True).get()

            # Atribuindo na variavel user o valor do usuario e a senha
            user = auth.authenticate(request, username=nome, password=senha)

            # Se o user estiver preenchido corretamente, iremos logar corretamente
            if user is not None:
                auth.login(request, user)
                # implementando mensagens de sucesso
                messages.success(request, 'Login realizado com sucesso')
                return redirect('dashboard')
            else:
                messages.error(
                    request, 'Email ou senha incorretos')
                return redirect('login')

        else:
            messages.error(
                request, 'Email não cadastrado')
            return redirect('login')
    return render(request, 'usuarios/login.html')


def dashboard(request):
    """ Encaminha a pessoa logada para sua página de dashboard """
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
    """ Realiza o logout do usuario """
    # Realizando logout do usuario e redirecionando ao index
    auth.logout(request)
    return redirect('index')


def campo_vazio(campo):
    """ Verifica se o campo é vazio ou não """
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    """ Verifica se as senhas são iguais ou não """
    return senha != senha2
