# Servidor Web em Python

Servidor Web desenvolvido em Python para a disciplina Redes II (AV1).

## Descrição

Este projeto implementa um servidor HTTP simples utilizando a biblioteca padrão do Python (`http.server`). O servidor oferece endpoints para testes de conectividade, echo de mensagens e cálculo de somas.

## Funcionalidades

- **GET /ping** - Verifica se o servidor está respondendo
- **GET /echo** - Retorna uma mensagem de cumprimento (com parâmetro opcional `name`)
- **POST /echo** - Retorna a mensagem recebida no corpo da requisição
- **POST /sum** - Calcula a soma de números recebidos

## Como Executar

### 1. Iniciar o servidor

```bash
python http_server.py
```

O servidor estará disponível em `http://localhost:8080`

## Testando os Endpoints

### GET /ping

```bash
curl http://localhost:8080/ping
```

Ou direto no navegador: http://localhost:8080/ping

### GET /echo com parâmetro

```bash
curl "http://localhost:8080/echo?name=Python"
```

Ou direto no navegador: http://localhost:8080/echo?name=Mundo

### POST /echo

```bash
curl -X POST http://localhost:8080/echo \
     -H "Content-Type: application/json" \
     -d '{"mensagem": "olá"}'
```

### POST /sum

```bash
curl -X POST http://localhost:8080/sum \
     -H "Content-Type: application/json" \
     -d '{"numbers": [1, 2, 3, 4, 5]}'
```

## Estrutura

- `http_server.py` - Arquivo principal com a implementação do servidor

## Requisitos

- Python 3.x

## Notas

O servidor utiliza a porta 8080 e escuta em todos os endereços disponíveis (0.0.0.0). Os logs das requisições são exibidos no terminal durante a execução.