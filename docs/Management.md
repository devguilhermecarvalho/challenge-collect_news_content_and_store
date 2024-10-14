# Gerenciamento de Tarefas

## Objetivo

Desenvolver um pipeline de coleta de dados de um site de notícias, disponibilizar os dados por meio de uma API, ingerir os dados no BigQuery, containerizar o projeto, e seguir os princípios de SOLID.

---

## Tarefas

### 1. **Coleta de Dados (Web Scraping)**

- [X] **Análise do site de notícias**
  - [X] Identificar estrutura HTML do site.
  - [X] Definir os dados a serem coletados (títulos, autores, datas, etc.).
- [X] **Implementar o Scraper**
  - [X] Verificar ferramentas (b4soup, scrapy) e princípios (ex: SOLID, Factory, Repository)
  - [X] Verificar a utilização do assincronismo para multi requisições
  - [X] Adicionar tratamento de erros (conexão, dados faltantes).

### 2. **Criação da API para disponibilizar os dados**

- [X] **Desenvolvimento da API**
  - [X] Implementar API com FastAPI.
- [X] **Testes**
  - [X] Testar endpoints com Postman.
  - [X] Garantir que os dados retornados estão no formato correto.

### 3. **Ingestão de Dados no BigQuery**

- [X] **Criação do Dataset no BigQuery**
  - [X] Criar dataset e tabela para armazenar os dados.
  - [X] Definir o schema das tabelas.
- [X] **Pipeline de Ingestão**
  - [X] Criar um script em Python para enviar os dados ao BigQuery.
  - [X] Utilizar bibliotecas como `google-cloud-bigquery`.
  - [X] Implementar verificações para evitar duplicações de dados.

### 4. **Containerização**

- [X] **Dockerização do projeto**
  - [X] Criar `Dockerfile` para a aplicação de scraping.
  - [X] Criar docker-compose para rodar o projeto completo (scraper, API, BigQuery).
  - [X] Testar containers localmente.

### 5. **Princípios de SOLID**

- [X] **Aplicação dos princípios de SOLID**
  - [X] Garantir a separação de responsabilidades no código.
  - [X] Implementar interfaces para abstração de conexões (API, BigQuery).
  - [X] Refatorar o código conforme necessário para garantir a coesão e baixo acoplamento.

### 6. **Documentação e Entrega**

- [X] **Documentação**
  - [X] Escrever README explicando o fluxo do projeto.
  - [X] Incluir exemplos de como rodar localmente e via Docker.
  - [X] Explicar como acessar a API e endpoints.

## Tecnologias Utilizadas

- Python (Web Scraping, API, Assincronismo, ETL/ELT)
- Docker (Containerização)
- Google Cloud (BigQuery)
- FastAPI (API)
- Postman (Testes de API)
- Git (Controle de Versão)
