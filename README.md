# ResolveDesk

Sistema web de chamados de suporte técnico desenvolvido com Python e Django.

O projeto permite registrar problemas, consultar chamados e acompanhar o andamento do atendimento. Está sendo desenvolvido como projeto de portfólio, com evolução gradual das funcionalidades.

## Funcionalidades disponíveis

- Abertura de chamados com título e descrição.
- Listagem dos chamados, do mais recente para o mais antigo.
- Registro automático da data de criação.
- Atualização do status: Aberto, Em andamento e Resolvido.

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

### 5. Iniciar o servidor de desenvolvimento

```bat
python manage.py runserver
```

Acesse a lista de chamados em:

http://127.0.0.1:8000/chamados/

O banco de dados local é criado pelas migrações e começa sem chamados.
O servidor utilizado nesta etapa é destinado ao desenvolvimento local.

## Próximas etapas

- Página de detalhes do chamado.
- Registro da solução aplicada.
- Autenticação e permissões de acesso.
- Pesquisa de soluções anteriores.
- Melhorias na interface.
- Testes automatizados das regras principais.

## Autor

Desenvolvido por Igor Delmasquio.

GitHub: https://github.com/JazzyJeff6