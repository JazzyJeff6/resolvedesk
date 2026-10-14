from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Chamado
from django.contrib.auth.models import Permission

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


    def test_novo_chamado_recebe_usuario_logado_como_autor(self):
        User = get_user_model()
        cliente = User.objects.create_user(username='cliente')

        permissao = Permission.objects.get(
            content_type__app_label='chamados',
            codename='add_chamado',
        )
        cliente.user_permissions.add(permissao)  

        self.client.force_login(cliente)

        resposta = self.client.post(
            reverse('novo_chamado'),
            {
                'titulo': 'Internet caindo',
                'descricao': 'A conexao cai durante o dia.',
            },
        )
        self.assertRedirects(resposta, reverse('listar_chamados'))

        self.assertEqual(Chamado.objects.count(), 1)

        chamado = Chamado.objects.get()
        self.assertEqual(chamado.autor_id, cliente.id)
        self.assertEqual(chamado.titulo, 'Internet caindo')
        self.assertEqual(chamado.status, 'aberto')


    def test_cliente_lista_apenas_os_proprios_chamados(self):
        User = get_user_model()

        cliente = User.objects.create_user(username='cliente')
        outro = User.objects.create_user(username='outro')

        proprio = Chamado.objects.create(
            titulo='Chamado do cliente',
            descricao='Problema do cliente logado.',
            autor=cliente,
        )

        Chamado.objects.create(
            titulo='Chamado de outro usuario',
            descricao='Problema de outra pessoa.',
            autor=outro,
        )

        self.client.force_login(cliente)

        resposta = self.client.get(reverse('listar_chamados'))

        self.assertEqual(resposta.status_code, 200)
        self.assertQuerySetEqual(
            resposta.context['chamados'],
            [proprio],
        )


    def test_busca_por_solucao_respeita_autor(self):
        User = get_user_model()

        cliente = User.objects.create_user(username='cliente')
        outro = User.objects.create_user(username='outro')

        proprio = Chamado.objects.create(
            titulo='Impressora nao imprime',
            descricao='A impressora nao responde.',
            solucao='Driver reinstalado.',
            autor=cliente,
        )

        Chamado.objects.create(
            titulo='Problema de outro cliente',
            descricao='Outro equipamento com falha.',
            solucao='Driver atualizado.',
            autor=outro,
        )

        Chamado.objects.create(
            titulo='Internet caindo',
            descricao='A conexao esta instavel.',
            solucao='Cabo substituido.',
            autor=cliente,
        )

        self.client.force_login(cliente)

        resposta = self.client.get(
            reverse('listar_chamados'),
            {'busca': 'driver'},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertQuerySetEqual(
            resposta.context['chamados'],
            [proprio],
        )

    def test_demonstracao_nao_cadastra_mesmo_com_permissao(self):
        User = get_user_model()
        demo = User.objects.create_user(username='cliente_demo')

        grupo = Group.objects.create(name='Demonstracao')
        demo.groups.add(grupo)

        permissao = Permission.objects.get(
            content_type__app_label='chamados',
            codename='add_chamado',
        )
        demo.user_permissions.add(permissao)

        self.client.force_login(demo)

        url = reverse('novo_chamado')

        resposta_get = self.client.get(url)
        self.assertEqual(resposta_get.status_code, 403)

        resposta_post = self.client.post(
            url,
            {
                'titulo': 'Tentativa de cadastro',
                'descricao': 'Enviado pela conta de demonstracao.',
            },
        )

        self.assertEqual(resposta_post.status_code, 403)
        self.assertEqual(Chamado.objects.count(), 0)

    def test_resumo_respeita_autor_e_nao_muda_com_busca(self):
        User = get_user_model()

        cliente = User.objects.create_user(username='cliente')
        outro = User.objects.create_user(username='outro')

        for status in ['aberto', 'em_andamento', 'resolvido']:
            Chamado.objects.create(
                titulo=f'Chamado {status}',
                descricao='Problema usado no teste.',
                autor=cliente,
                status=status,
            )

        Chamado.objects.create(
            titulo='Chamado de outra pessoa',
            descricao='Nao deve entrar nos contadores do cliente.',
            autor=outro,
            status='resolvido',
        )

        self.client.force_login(cliente)

        esperado = {
            'abertos': 1,
            'em_andamento': 1,
            'resolvidos': 1,
        }

        resposta = self.client.get(reverse('listar_chamados'))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['resumo'], esperado)

        resposta_busca = self.client.get(
            reverse('listar_chamados'),
            {'busca': 'sem correspondencia'},
        )

        self.assertEqual(resposta_busca.status_code, 200)
        self.assertEqual(resposta_busca.context['resumo'], esperado)
        self.assertEqual(resposta_busca.context['chamados'].count(), 0)

    def test_filtro_status_combina_busca_e_respeita_autor(self):
        User = get_user_model()
        cliente = User.objects.create_user(username='cliente')
        outro = User.objects.create_user(username='outro')

        esperado = Chamado.objects.create(
            titulo='Impressora do financeiro',
            descricao='Falha na impressao.',
            autor=cliente,
            status='resolvido',
        )

        Chamado.objects.create(
            titulo='Impressora da recepcao',
            descricao='Falha na impressao.',
            autor=cliente,
            status='aberto',
        )

        Chamado.objects.create(
            titulo='Internet instavel',
            descricao='Falha na conexao.',
            autor=cliente,
            status='resolvido',
        )

        Chamado.objects.create(
            titulo='Impressora de outro cliente',
            descricao='Falha na impressao.',
            autor=outro,
            status='resolvido',
        )

        self.client.force_login(cliente)

        resposta = self.client.get(
            reverse('listar_chamados'),
            {'busca': 'impressora', 'status': 'resolvido'},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertQuerySetEqual(
            resposta.context['chamados'],
            [esperado],
        )
        self.assertEqual(
            resposta.context['status_selecionado'],
            'resolvido',
        )
        self.assertEqual(
            resposta.context['resumo'],
            {'abertos': 1, 'em_andamento': 0, 'resolvidos': 2},
        )