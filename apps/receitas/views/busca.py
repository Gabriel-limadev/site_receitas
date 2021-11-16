from django.shortcuts import get_object_or_404, render, redirect
from receitas.models import Receita


def busca(request):
    """ Realiza a busca de uma receita """
    lista_receitas = Receita.objects.order_by(
        '-date_receita').filter(publicada=True)

    if 'busca' in request.GET:
        nome_busca = request.GET['busca']
        lista_receitas = lista_receitas.filter(
            nome_receita__icontains=nome_busca)

    dados = {
        'receitas': lista_receitas
    }
    return render(request, 'receitas/busca.html', dados)
