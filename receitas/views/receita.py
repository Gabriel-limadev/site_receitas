from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

# Create your views here.


def index(request):
    receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)

    dados = {
        'receitas': receitas
    }

    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_exibir = {
        'receita': receita
    }
    return render(request, 'receitas/receita.html', receita_exibir)


def cria_receita(request):
    if request.method == "POST":
        # Pegando os dados vindo do usuario
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']

        # Implementando mensagens de erro
        if campo_vazio(nome_receita) or campo_vazio(ingredientes) or campo_vazio(modo_preparo) or campo_vazio(rendimento) or campo_vazio(categoria):
            messages.error(
                request, 'Os campos não podem ficar em branco')
            dados = {
                'nome_receita': nome_receita,
                'ingredientes': ingredientes,
                'modo_preparo': modo_preparo,
                'tempo_preparo': tempo_preparo,
                'rendimento': rendimento,
                'categoria': categoria,
            }

            return render(request, 'receitas/cria_receita.html', dados)

        # Salvando dados
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(
            pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()

        # Redirecionando ao dashboard
        return redirect('dashboard')

    else:
        return render(request, 'receitas/cria_receita.html  ')


def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}

    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)

        # Pegando os dados vindo do usuario
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']

        # Implementando mensagens de erro
        if campo_vazio(r.nome_receita) or campo_vazio(r.ingredientes) or campo_vazio(r.modo_preparo) or campo_vazio(r.rendimento) or campo_vazio(r.categoria):
            messages.error(
                request, 'Os campos não podem ficar em branco')

            receita = get_object_or_404(Receita, pk=receita_id)
            receita_a_editar = {'receita': receita}
            return render(request, 'receitas/edita_receita.html', receita_a_editar)

        # Salvando
        r.save()
        return redirect('dashboard')


def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')
