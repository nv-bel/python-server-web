# Servidor Web em Python

Servidor Web desenvolvido em Python para a disciplina Redes II (AV1).

## Descrição

Este projeto implementa um servidor HTTP simples com socket TCP e roteamento manual. O servidor exibe uma interface web para buscar usuários por ID (GET) e cadastrar novos usuários (POST).

## Funcionalidades

- **GET /** - Página principal com formulário para buscar usuário por ID e cadastrar um novo usuário
- **GET /** com `?id=<valor>` - Busca um usuário existente em `data/dados.json`
- **POST /** - Recebe dados de formulário (`nome`, `idade`) e salva um novo usuário em `data/dados.json`
- **GET /static/styles.css** - Serve o CSS da interface

## Como Executar

### 1. Iniciar o servidor

```bash
python app.py
```

O servidor estará disponível em `http://127.0.0.1:8080`.

## Testando a Aplicação

### Acessar a página principal

Abra no navegador:

```text
http://127.0.0.1:8080/
```

### Buscar usuário por ID

No navegador, use a URL:

```text
http://127.0.0.1:8080/?id=1
```

### Cadastrar novo usuário

Na página principal, use o formulário de cadastro com os campos `nome` e `idade`.

## Estrutura do Projeto

- `app.py` - Inicializa o servidor TCP e processa as requisições
- `routes.py` - Lógica de roteamento, renderização de templates e resposta HTTP
- `storage.py` - Funções para carregar e salvar dados em `data/dados.json`
- `templates/` - Templates HTML para a página principal e confirmação de cadastro
- `static/` - Arquivos estáticos, como o CSS
- `data/dados.json` - Armazena os usuários cadastrados

## Requisitos

- Python 3.x

## Observações

- A pasta `old_http_server/` não faz parte da implementação atual e deve ser desconsiderada.
- O servidor utiliza a porta `8080` e responde em `127.0.0.1`.
- Os acessos e ações são logados no terminal durante a execução.
