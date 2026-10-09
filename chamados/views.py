from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChamadoForm, ChamadoStatusForm, ChamadoSolucaoForm
from .models import Chamado
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
# Create your views here.

from django.shortcuts import render, redirect
from .forms import ChamadoForm

def usuario_e_tecnico(user):
    return(
        user.is_superuser
        or
        user.groups.filter(name='Tecnicos').exists()
    )


@login_required
def novo_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)

        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.autor = request.user
            chamado.save()
            return redirect('listar_chamados')
    else:
        form = ChamadoForm()
    
    return render(request, 'chamados/novo_chamado.html', {'form':form})


@login_required
def listar_chamados(request):
    busca = request.GET.get('busca', '').strip()

    chamados = Chamado.objects.order_by('-criado_em')

    if not usuario_e_tecnico(request.user):
        chamados = chamados.filter(autor=request.user)

    if busca:
        chamados = chamados.filter(
            Q(titulo__icontains=busca) 
            | Q(descricao__icontains=busca)
            | Q(solucao__icontains=busca)
        )

    return render(
        request,
        'chamados/listar_chamados.html',
        {
        'chamados': chamados, 'busca': busca, 'e_tecnico': usuario_e_tecnico(request.user),
        },
    )


@login_required
def atualizar_status(request, chamado_id):
    if not usuario_e_tecnico(request.user):
        raise PermissionDenied

    
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


@login_required
def detalhe_chamado(request, chamado_id):
    chamados = Chamado.objects.all()

    if not usuario_e_tecnico(request.user):
        chamados = chamados.filter(autor=request.user)

    chamado = get_object_or_404(chamados, pk=chamado_id)

    return render(
        request,
        'chamados/detalhe_chamado.html',
        {
            'chamado': chamado,
            'e_tecnico': usuario_e_tecnico(request.user),
        },
    )


@login_required
def registrar_solucao(request, chamado_id):
    if not usuario_e_tecnico(request.user):
        raise PermissionDenied

    chamado = get_object_or_404(Chamado, pk=chamado_id)

    if request.method == 'POST':
        form = ChamadoSolucaoForm(request.POST, instance=chamado)
                                  
        if form.is_valid():
            form.save()
            return redirect('detalhe_chamado', chamado_id=chamado.id)
    else:
        form = ChamadoSolucaoForm(instance=chamado)

    return render(
        request,
        'chamados/registar_solucao.html',
        {
            'form': form, 'chamado': chamado, 'e_tecnico': usuario_e_tecnico(request.user),
        },
    )