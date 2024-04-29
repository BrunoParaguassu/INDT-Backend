# Sistema de Gerenciamento de Usuário

Este é um sistema de gerenciamento de usuário desenvolvido em Python com Flask para o back-end e ReactJS para o front-end. O sistema permite a criação, leitura, atualização e exclusão de usuários, além de fornecer um sistema de autenticação com tokens JWT.

## Configuração do Ambiente

### Back-end (Flask)

1. Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
2. Instale as dependências do back-end executando o comando `pip install -r requirements.txt`.
3. Configure a conexão com o banco de dados PostgreSQL no arquivo `app.py`.
4. Execute as migrações do banco de dados executando o comando `python manage.py db upgrade`.

### Front-end (ReactJS)

1. Certifique-se de ter o Node.js instalado em seu sistema. Você pode baixá-lo em [nodejs.org](https://nodejs.org/).
2. Navegue até o diretório `frontend` e instale as dependências do front-end executando o comando `npm install`.

## Executando o Projeto

1. Para iniciar o back-end, execute o comando `python app.py` na raiz do projeto.
2. Para iniciar o front-end, navegue até o diretório `frontend` e execute o comando `npm start`.

## Testes

1. Os testes unitários estão localizados no arquivo `test_app.py` na raiz do projeto.
2. Para executar os testes, instale o pytest executando o comando `pip install pytest` e execute o comando `pytest` na raiz do projeto.

## Documentação Adicional

- A lógica de autenticação do back-end utiliza tokens JWT. Certifique-se de manter a chave secreta JWT (`JWT_SECRET_KEY`) segura e nunca a exponha publicamente.
- A aplicação front-end utiliza D3chart para a criação de gráficos de usuários ativos e cancelados. Você pode encontrar a documentação de D3chart em [d3js.org](https://d3js.org/).

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests com melhorias, correções de bugs ou novas funcionalidades.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
