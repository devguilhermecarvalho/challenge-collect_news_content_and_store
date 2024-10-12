# Gerenciamento de Tarefas - Projeto de Engenharia de Dados

## Objetivo

Desenvolver um pipeline de coleta de dados de um site de notícias, disponibilizar os dados por meio de uma API, ingerir os dados no BigQuery, containerizar o projeto, e seguir os princípios de SOLID.

---

## Tarefas

### 1. **Coleta de Dados (Web Scraping)**

- [ ] **Análise do site de notícias**
  - [ ] Identificar estrutura HTML do site.
  - [ ] Definir os dados a serem coletados (títulos, autores, datas, etc.).
- [ ] **Implementar o Scraper**
  - [ ] Escolher a ferramenta de scraping (BeautifulSoup, Scrapy, etc.).
  - [ ] Criar classe para scraping seguindo princípios de SOLID.
  - [ ] Adicionar tratamento de erros (conexão, dados faltantes).
  - [ ] Testar o scraper em diferentes artigos.

### 2. **Criação da API para disponibilizar os dados**

- [ ] **Desenho da API**
  - [ ] Definir os endpoints para consulta dos dados (GET, POST, etc.).
  - [ ] Criar arquitetura RESTful.
- [ ] **Desenvolvimento da API**
  - [ ] Implementar API com FastAPI/Flask.
  - [ ] Implementar autenticação (se necessário).
  - [ ] Implementar boas práticas de rotas e segurança.
  - [ ] Containerizar a API usando Docker.
  - [ ] Documentar a API (Swagger/OpenAPI).
- [ ] **Testes**
  - [ ] Testar endpoints com Postman.
  - [ ] Garantir que os dados retornados estão no formato correto.

### 3. **Ingestão de Dados no BigQuery**

- [ ] **Criação do Dataset no BigQuery**
  - [ ] Criar dataset e tabela para armazenar os dados.
  - [ ] Definir o schema das tabelas.
- [ ] **Pipeline de Ingestão**
  - [ ] Criar um script em Python para enviar os dados ao BigQuery.
  - [ ] Utilizar bibliotecas como `google-cloud-bigquery`.
  - [ ] Testar a ingestão de dados (pequenos lotes de dados).
  - [ ] Implementar verificações para evitar duplicações de dados.

### 4. **Containerização**

- [ ] **Dockerização do projeto**
  - [ ] Criar `Dockerfile` para a aplicação de scraping.
  - [ ] Criar `Dockerfile` para a API.
  - [ ] Criar docker-compose para rodar o projeto completo (scraper, API, BigQuery).
  - [ ] Testar containers localmente.

### 5. **Princípios de SOLID**

- [ ] **Aplicação dos princípios de SOLID**
  - [ ] Garantir a separação de responsabilidades no código.
  - [ ] Implementar interfaces para abstração de conexões (API, BigQuery).
  - [ ] Refatorar o código conforme necessário para garantir a coesão e baixo acoplamento.

### 6. **Automatização do Pipeline**

- [ ] **Cloud Functions/Cloud Run**
  - [ ] Automatizar o scraper para rodar periodicamente (Cloud Scheduler ou similar).
  - [ ] Enviar os dados automaticamente para o BigQuery após a coleta.
  - [ ] Testar a execução automatizada.

### 7. **Monitoramento e Logging**

- [ ] **Monitoramento do Pipeline**
  - [ ] Implementar logs detalhados (utilizar `logging` em Python).
  - [ ] Criar um painel de monitoramento no BigQuery (Looker Studio ou outro).

### 8. **Documentação e Entrega**

- [ ] **Documentação**
  - [ ] Escrever README explicando o fluxo do projeto.
  - [ ] Incluir exemplos de como rodar localmente e via Docker.
  - [ ] Explicar como acessar a API e endpoints.
  - [ ] Documentar testes realizados.

---

## Estrutura de Pastas Proposta

## Cronograma

| Fase                     | Início    | Término   |
| ------------------------ | ---------- | ---------- |
| Coleta de Dados          | DD/MM/YYYY | DD/MM/YYYY |
| Criação da API         | DD/MM/YYYY | DD/MM/YYYY |
| Ingestão no BigQuery    | DD/MM/YYYY | DD/MM/YYYY |
| Containerização        | DD/MM/YYYY | DD/MM/YYYY |
| Automação e Testes     | DD/MM/YYYY | DD/MM/YYYY |
| Documentação e Entrega | DD/MM/YYYY | DD/MM/YYYY |

## Tecnologias Utilizadas

- Python (Web Scraping, API)
- Docker (Containerização)
- Google Cloud (BigQuery, Cloud Functions)
- FastAPI/Flask (API)
- Postman (Testes de API)
- Git (Controle de Versão)
