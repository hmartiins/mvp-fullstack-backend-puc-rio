# Controle de Gastos Pessoais — API

API REST desenvolvida em Python + Flask para registro e consulta de gastos pessoais organizados por categorias. Utiliza SQLite como banco de dados e expõe documentação interativa via Swagger.

---

## Funcionalidades

- Cadastro e listagem de **categorias** (ex.: Alimentação, Transporte, Lazer)
- Registro de **despesas** com valor, data e descrição vinculada a uma categoria
- Consulta de **resumo de gastos por categoria**
- Filtragem de despesas por **intervalo de datas**
- Documentação Swagger em `/docs`

---

## Pré-requisitos

- Python 3.10 ou superior
- pip

---

## Instalação

### 1. Clone ou copie o projeto

```bash
cd controle-gastos-api
```

### 2. Crie e ative o ambiente virtual

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Iniciando o servidor

```bash
python app.py
```

O servidor iniciará em `http://localhost:5000`.
O banco de dados `gastos.db` será criado automaticamente na primeira execução.

---

## Documentação Swagger

Acesse a interface interativa com todos os endpoints documentados:

```
http://localhost:5000/docs
```

---

## Rotas disponíveis

### Categorias

| Método | Rota                    | Descrição                     |
|--------|-------------------------|-------------------------------|
| POST   | `/categorias`           | Cadastrar nova categoria       |
| GET    | `/categorias`           | Listar todas as categorias     |
| DELETE | `/categorias/<id>`      | Deletar uma categoria          |

### Despesas

| Método | Rota                    | Descrição                              |
|--------|-------------------------|----------------------------------------|
| POST   | `/despesas`             | Cadastrar nova despesa                 |
| GET    | `/despesas`             | Listar todas as despesas               |
| GET    | `/despesas/<id>`        | Buscar despesa por ID                  |
| DELETE | `/despesas/<id>`        | Deletar uma despesa                    |
| GET    | `/despesas/resumo`      | Total gasto por categoria              |
| GET    | `/despesas/periodo`     | Filtrar por período (`data_inicio` e `data_fim` como query params) |

---

## Exemplos de uso

### Criar categoria

```bash
curl -X POST http://localhost:5000/categorias \
  -H "Content-Type: application/json" \
  -d '{"nome": "Alimentação", "descricao": "Refeições e mercado"}'
```

### Criar despesa

```bash
curl -X POST http://localhost:5000/despesas \
  -H "Content-Type: application/json" \
  -d '{"descricao": "Almoço", "valor": 35.50, "data": "2024-03-15", "categoria_id": 1}'
```

### Filtrar por período

```bash
curl "http://localhost:5000/despesas/periodo?data_inicio=2024-01-01&data_fim=2024-12-31"
```

---

## Estrutura do projeto

```
controle-gastos-api/
├── app.py           # Rotas, lógica da API e configuração Swagger
├── models.py        # Conexão com SQLite e inicialização do banco
├── requirements.txt # Dependências Python
└── README.md        # Este arquivo
```

---

## Banco de dados

O arquivo `gastos.db` é gerado automaticamente. O esquema possui duas tabelas:

- **categorias** — `id`, `nome` (único), `descricao`
- **despesas** — `id`, `descricao`, `valor`, `data`, `categoria_id` (FK → categorias)
