from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Chamado

class AcessoChamadosTests(TestCase):
    def test_visitante_e_redirecionado_para_login(self):
        resposta = self.client.get(reverse('listar_chamados'))

        destino = (
            f"{reverse('login')}?next={reverse('listar_chamados')}"
        )

        self.assertRedirects(resposta, destino)

    def test_client_nao_acessa_chamado_de_outro_usuario(self):
        User = get_user_model()

        cliente = User.objects.create_user(username='cliente')
        outro_usuario = User.objects.create_user(username='outro')

        chamado = Chamado.objects.create(
            titulo='Problema de outro usuario',
            descricao='Chamado usado no teste de acesso',
            autor=outro_usuario
        )

        self.client.force_login(cliente)

        resposta = self.client.get(
            reverse('detalhe_chamado', args=[chamado.id])
        )

        self.assertEqual(resposta.status_code, 404)



    def test_cliente_nao_altera_status_do_proprio_chamado(self):
        User = get_user_model()
        cliente = User.objects.create_user(username='cliente')

        chamado = Chamado.objects.create(
            titulo='Internet caindo',
            descricao='A conexao cai durante o dia.',
            autor=cliente,
            status='aberto',
        )

        self.client.force_login(cliente)

        resposta = self.client.post(
            reverse('atualizar_status', args=[chamado.id]),
            {'status': 'resolvido'},
        )

        self.assertEqual(resposta.status_code, 403)

        chamado.refresh_from_db()
        self.assertEqual(chamado.status, 'aberto')

    def test_tecnico_altera_status_de_chamado(self):
        User = get_user_model()

        cliente = User.objects.create_user(username='cliente')
        tecnico = User.objects.create_user(username='tecnico')

        grupo = Group.objects.create(name='Tecnicos')
        tecnico.groups.add(grupo)

        chamado = Chamado.objects.create(
            titulo='Impressora nao imprime',
            descricao='A impressora nao responde.',
            autor=cliente,
            status='aberto',
        )

        self.client.force_login(tecnico)

        resposta = self.client.post(
            reverse('atualizar_status', args=[chamado.id]),
            {'status': 'em_andamento'},
        )

        self.assertRedirects(resposta, reverse('listar_chamados'))

        chamado.refresh_from_db()
        self.assertEqual(chamado.status, 'em_andamento')

    def test_tecnico_altera_status_de_chamado(self):
        User = get_user_model()

        cliente = User.objects.create_user(username='cliente')
        tecnico = User.objects.create_user(username='tecnico')

        grupo = Group.objects.create(name='Tecnicos')
        tecnico.groups.add(grupo)

        chamado = Chamado.objects.create(
            titulo='Impressora nao imprime',
            descricao='A impressora nao responde.',
            autor=cliente,
            status='aberto',
        )

        self.client.force_login(tecnico)

        resposta = self.client.post(
            reverse('atualizar_status', args=[chamado.id]),
            {'status': 'em_andamento'},
        )

        self.assertRedirects(resposta, reverse('listar_chamados'))

        chamado.refresh_from_db()
        self.assertEqual(chamado.status, 'em_andamento')


    def test_cliente_nao_altera_solucao_do_proprio_chamado(self):
        User = get_user_model()
        cliente = User.objects.create_user(username='cliente')

        chamado = Chamado.objects.create(
            titulo='Impressora nao imprime',
            descricao='A impressora nao responde.',
            autor=cliente,
            solucao='Solucao registrada pelo tecnico.',
        )

        self.client.force_login(cliente)

        resposta = self.client.post(
            reverse('registrar_solucao', args=[chamado.id]),
            {'solucao': 'Alteracao feita pelo cliente.'},
        )

        self.assertEqual(resposta.status_code, 403)

        chamado.refresh_from_db()
        self.assertEqual(
            chamado.solucao,
            'Solucao registrada pelo tecnico.',
        )


    def test_tecnico_altera_solucao_de_chamado(self):
        User = get_user_model()

        cliente = User.objects.create_user(username='cliente')
        tecnico = User.objects.create_user(username='tecnico')

        grupo = Group.objects.create(name='Tecnicos')
        tecnico.groups.add(grupo)

        chamado = Chamado.objects.create(
            titulo='Impressora nao imprime',
            descricao='A impressora nao responde.',
            autor=cliente,
            solucao='',
        )

        self.client.force_login(tecnico)

        resposta = self.client.post(
            reverse('registrar_solucao', args=[chamado.id]),
            {'solucao': 'Driver reinstalado e impressao testada.'},
        )

        self.assertRedirects(
            resposta,
            reverse('detalhe_chamado', args=[chamado.id]),
        )

        chamado.refresh_from_db()
        self.assertEqual(
            chamado.solucao,
            'Driver reinstalado e impressao testada.',
        )
        self.assertEqual(chamado.autor_id, cliente.id)