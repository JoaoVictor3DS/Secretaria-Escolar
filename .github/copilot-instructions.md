# Copilot Instructions for Secretaria-Escolar

## Visão Geral da Arquitetura

- Projeto Django para gestão escolar, com apps e módulos organizados em `projeto/`.
- Fluxo principal: views (em `projeto/views.py`) recebem requisições, usam models (`projeto/models.py`) e serializers (`projeto/serializers.py`), retornando respostas para templates em `projeto/templates/`.
- Arquivos estáticos e uploads são servidos via `static/` e `media/`.
- URLs principais estão em `SecretariaEscolar/urls.py` e roteiam para views do app.

## Fluxos de Desenvolvimento

- **Rodar o servidor:**
  ```bash
  python manage.py runserver
  ```
- **Migrações:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- **Criar superusuário:**
  ```bash
  python manage.py createsuperuser
  ```
- **Testes:**
  ```bash
  python manage.py test
  ```
- **Scripts customizados:**
  Use comandos em `projeto/management/commands/` via `python manage.py <comando>`.

## Convenções Específicas

- Nomes e comentários em português, refletindo o domínio escolar.
- Templates HTML em `projeto/templates/` e `homeUp/`.
- Uploads de arquivos (contratos, imagens) em subpastas de `media/`.
- Models e views centralizam regras de negócio; serializers para APIs.
- Scripts de setup de grupos/permissões em `projeto/management/commands/setup_groups.py`.

## Integrações e Dependências

- Dependências listadas em `requirements.txt`.
- Configurações em `SecretariaEscolar/settings.py`.
- Banco SQLite padrão (`db.sqlite3`).

## Exemplos de Padrões

- **View:**
  ```python
  # projeto/views.py
  def minha_view(request):
      # ...lógica...
      return render(request, 'template.html', contexto)
  ```
- **Model:**
  ```python
  # projeto/models.py
  class Aluno(models.Model):
      nome = models.CharField(max_length=100)
  ```

Se alguma seção estiver incompleta ou pouco clara, por favor, informe para que eu possa aprimorar as instruções!
