from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChamadoForm, ChamadoStatusForm
from .models import Chamado

# Create your views here.

from django.shortcuts import render, redirect
from .forms import ChamadoForm

def novo_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_chamados')
    else:
        form = ChamadoForm()
    
    return render(request, 'chamados/novo_chamado.html', {'form':form})

def listar_chamados(request):
    chamados = Chamado.objects.order_by('-criado_em')

    return render(
        request,
        'chamados/listar_chamados.html',
        {'chamados': chamados}
    )

def atualizar_status(request, chamado_id):
    chamado = get_object_or_404(Chamado, pk=chamado_id)

    if request.method == 'POST':
        form = ChamadoStatusForm(request.POST, instance=chamado)

        if form.is_valid():
            form.save()
            return redirect('listar_chamados')
    else:
        form = ChamadoStatusForm(instance=chamado)

    return render(
        request,
        'chamados/atualizar_status.html',
        {'form': form, 'chamado': chamado}
    )
            