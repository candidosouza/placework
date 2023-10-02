# placework
Respositório destinado ao cadastro e login para app  PlaceWork

## Índice

- [Bibliotecas utilizadas](#bibliotecas-utilizadas)
- [Instalação](#instalação)
- [Utilização](#utilização)
- [Informações Importantes](#informações-importantes)

## Bibliotecas utilizadas

- [Django](https://www.djangoproject.com/)
Framework para desenvolvimento rápido para web, escrito em Python, que utiliza o padrão model-template-view
- [Poetry](https://python-poetry.org/)
Gerenciador de dependências e empacotador de projetos para Python
- [Taskpy](https://github.com/taskipy/taskipy)
Ferramenta para automatizar alguns comandos e simplificar o fluxo
- [Ruff](https://docs.astral.sh/ruff/)
Um linter, para dizer se não estamos fazendo nada de errado no código
- [Blue](https://blue.readthedocs.io/en/latest/index.html)
Um formatador de código bastante amigável
- [Isort](https://pycqa.github.io/isort/)
Uma ferramenta para ordenar os imports em ordem alfabética
- [Pytest](https://docs.pytest.org/en/7.4.x/)
Framework de testes para Python
- [Faker](https://github.com/joke2k/faker)
Biblioteca para gerar dados fakes
- [MailTrap](https://mailtrap.io/)
Biblioteca para envio de e-mail para desenvolvimento
- [Laravel-mix](https://laravel-mix.com/)
Empacotador de módulos que prepara o JavaScript, css, imagens e demais ativos para o navegador
-[Bootstrap](https://getbootstrap.com/)
Framework front-end para desenvolvimento de componentes de interface e front-end para sites e aplicações web usando HTML, CSS e JavaScript
- [SonarCloud](https://sonarcloud.io/)
Ferramenta de análise estática de código


## Instalação

### Pré-requisitos
Docker

### Instalação
1. Clone o repositório
2. Execute o comando `docker-compose up -d --build`
3. Execute o comando `docker-compose exec app python bash`
4. Execute o comando `poetry install`
4. Execute o comando `poetry shell`
5. Execute o comando `python manage.py migrate`
6. Execute o comando `python manage.py seeds` para dados fakes
7. Execute o comando `python manage.py runserver 0.0.0.0:8000`


## Utilização

App: [http://localhost:8000](http://localhost:8000/)

Pg Admin: [http://localhost:5050](http://localhost:5050/)

Container Postgres: `docker-compose exec db bash`


## Informações Importantes

- Algumas informações sobre os arquivos e pastas do projeto:
    - `common/` - Pasta com arquivos em comuns a todos os apps do projeto
    - `setup/` - Pasta com arquivos de configuração do projeto
    - `placework/` - Pasta com arquivos do app