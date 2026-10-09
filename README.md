# ResolveDesk

Sistema web de chamados de suporte técnico desenvolvido com Python e Django.

O projeto permite registrar problemas, consultar chamados e acompanhar o andamento do atendimento. Está sendo desenvolvido como projeto de portfólio, com evolução gradual das funcionalidades.

## Funcionalidades disponíveis

- Abertura de chamados com título e descrição.
- Listagem dos chamados, do mais recente para o mais antigo.
- Página de detalhes de cada chamado.
- Registro automático da data de criação.
- Atualização do status: Aberto, Em andamento e Resolvido.
- Registro e edição da solução aplicada.
- Pesquisa por texto no título, na descrição e na solução.
- Login e logout de usuários.
- Exigência de autenticação para acessar os chamados.
- Associação automática de novos chamados ao usuário que os abriu.
- Clientes acessam somente os próprios chamados.
- Técnicos e administradores consultam todos os chamados e podem
  atualizar status e registrar soluções.
- Verificação de permissões no backend, inclusive no acesso direto às URLs.

## Tecnologias

- Python
- Django
- SQLite
- HTML com templates do Django
- Git e GitHub

## Como executar no Windows

Os comandos abaixo devem ser executados no Prompt de Comando (CMD).
É necessário ter Python e Git instalados.

### 1. Clonar o repositório

```bat
git clone https://github.com/JazzyJeff6/resolvedesk.git
cd resolvedesk
```

### 2. Criar e ativar o ambiente virtual

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instalar as dependências

```bat
python -m pip install -r requirements.txt
```

### 4. Preparar o banco de dados

```bat
python manage.py migrate
```

### Criar uma conta administradora

```bat
python manage.py createsuperuser
```

Depois de iniciar o servidor, entre com essa conta em:

http://127.0.0.1:8000/admin/

No painel administrativo, é possível criar usuários e grupos:

- **Cliente:** usuário ativo, sem privilégios administrativos e fora
  do grupo `Tecnicos`.
- **Técnico:** usuário ativo pertencente ao grupo `Tecnicos`.
  Não precisa ser staff ou superusuário.
- **Administrador:** conta criada com `createsuperuser`.

O nome do grupo deve ser exatamente `Tecnicos`, sem acento.


### 6. Iniciar o servidor de desenvolvimento

```bat
python manage.py runserver
```

Acesse a lista de chamados em:

http://127.0.0.1:8000/chamados/

O banco de dados local é criado pelas migrações e começa sem chamados.
O servidor utilizado nesta etapa é destinado ao desenvolvimento local.

## Próximas etapas

- Melhorias na interface com CSS.
- Biblioteca dedicada de soluções.
- Sugestões de soluções por semelhança entre chamados.
- Testes automatizados das regras principais.

## Autor

Desenvolvido por Igor Delmasquio.

GitHub: https://github.com/JazzyJeff6