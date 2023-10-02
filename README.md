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
<!-- - [SonarCloud](https://sonarcloud.io/)
Ferramenta de análise estática de código -->


## Instalação

### Pré-requisitos
Docker

### Instalação

1. Clone o repositório

```bash
git clone https://github.com/candidosouza/placework.git
```
2. Acesse a pasta do projeto

```bash
cd placework
```
3. Execute o comando 

```bash
docker-compose up -d --build
```

4. Execute o comando para entrar no container da aplicação

```bash
docker-compose exec app bash
```

5. Execute o comando para instalar as dependências

```bash
poetry install
```

6. Ativar o ambiente virtual

```bash
poetry shell
```

7. Rodar as migrações
```bash
python manage.py migrate
```
8. Rodar as fixtures
```bash
python manage.py seeds
```
9. Rodar o servidor

```bash
 python manage.py runserver 0.0.0.0:8000
```

10. Acesse o sistema em [http://localhost:8000](http://localhost:8000/)

11. Acesse o pgadmin em [http://localhost:5050](http://localhost:5050/)

12. Acesse o container do postgres

```bash
docker-compose exec db bash
```

### Em caso de problemas com a estilização

Entrar na pasta do projeto e rodar o comando:

```bash
npm install
```
e após a instalação, rodar o comando:

```bash
npm run watch
```

### Acesso ao admin

- Usuário: admin
- Senha: admin

[http://localhost:8000/admin-placework/](http://localhost:8000/admin-placework/)


#### Para envio de emails:

O sistema foi configurado usando o MailTrap, para que os emails sejam enviados, é necessário configurar as variáveis de ambiente no arquivo `.env`:

link: [https://mailtrap.io/](https://mailtrap.io/)

váriáveis necessárias:

- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD


## Informações Importantes

- Algumas informações sobre os arquivos e pastas do projeto:
    - `common/` - Pasta com arquivos em comuns a todos os apps do projeto
    - `setup/` - Pasta com arquivos de configuração do projeto
    - `placework/` - Pasta com arquivos do app
