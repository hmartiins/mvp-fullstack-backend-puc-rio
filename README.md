# Controle de Gastos Pessoais — API

API REST desenvolvida em **Python + Flask** para registro e consulta de gastos pessoais organizados por categorias. Utiliza **SQLite** como banco de dados, **SQLAlchemy** como ORM e expõe documentação interativa via **OpenAPI 3.0 (Swagger UI)**.

---

## Funcionalidades

- Cadastro e listagem de **categorias** (ex.: Alimentação, Transporte, Lazer)
- Registro de **despesas** com valor, data e descrição vinculada a uma categoria
- Consulta de **resumo de gastos por categoria**
- Filtragem de despesas por **intervalo de datas**
- Validação automática de tipos e campos obrigatórios via **Pydantic**
- Documentação interativa disponível em `/docs/swagger`

---

## Pré-requisitos

- **[Python 3.10](https://www.python.org/downloads/release/python-3100/)** ou superior
- **pip3**

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/hmartiins/mvp-fullstack-backend-puc-rio.git
cd mvp-fullstack-backend-puc-rio
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
python3 app.py
```

O servidor iniciará em `http://localhost:5001`.  
O banco de dados será criado automaticamente em `database/gastos.db` na primeira execução.

---

## Documentação

Acesse a interface interativa (Swagger) com todos os endpoints documentados:

```
http://localhost:5001/docs/swagger
```

---

## Rotas disponíveis

### Categorias

| Método   | Rota               | Descrição                  |
| -------- | ------------------ | -------------------------- |
| `POST`   | `/categorias`      | Cadastrar nova categoria   |
| `GET`    | `/categorias`      | Listar todas as categorias |
| `DELETE` | `/categorias/<id>` | Deletar uma categoria      |

### Despesas

| Método   | Rota                | Descrição                                                      |
| -------- | ------------------- | -------------------------------------------------------------- |
| `POST`   | `/despesas`         | Cadastrar nova despesa                                         |
| `GET`    | `/despesas`         | Listar todas as despesas                                       |
| `GET`    | `/despesas/<id>`    | Buscar despesa por ID                                          |
| `DELETE` | `/despesas/<id>`    | Deletar uma despesa                                            |
| `GET`    | `/despesas/resumo`  | Total gasto por categoria                                      |
| `GET`    | `/despesas/periodo` | Filtrar por período (query params: `data_inicio` e `data_fim`) |

---

## Exemplos de uso

### Criar categoria

```bash
curl -X POST http://localhost:5001/categorias \
  -H "Content-Type: application/json" \
  -d '{"nome": "Alimentação", "descricao": "Refeições e mercado"}'
```

### Criar despesa

```bash
curl -X POST http://localhost:5001/despesas \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Almoço",
    "valor": 35.50,
    "data": "2024-03-15",
    "categoria_id": "<uuid-da-categoria>"
  }'
```

### Filtrar por período

```bash
curl "http://localhost:5001/despesas/periodo?data_inicio=2024-01-01&data_fim=2024-12-31"
```

---

## Estrutura do projeto

```
controle-gastos-api/
├── app.py                  # Configuração da aplicação e handlers globais
├── utils.py                # Funções utilitárias
├── requirements.txt        # Dependências Python
├── model/
│   └── models.py           # Modelos SQLAlchemy (Categoria, Despesa)
├── schemas/
│   ├── categoria.py        # Schemas Pydantic de categorias
│   ├── despesa.py          # Schemas Pydantic de despesas
│   └── comum.py            # Schemas de resposta compartilhados
├── service/
│   ├── categoria_service.py  # Lógica de negócio de categorias
│   ├── despesa_service.py    # Lógica de negócio de despesas
│   └── exceptions.py         # Exceções de domínio (NotFoundError, ConflictError)
├── routes/
│   ├── categorias/         # Endpoints de categorias
│   └── despesas/           # Endpoints de despesas
├── database/               # Banco de dados SQLite (gerado automaticamente)
└── .github/
    └── workflows/
        └── ci.yml          # Pipeline de CI (GitHub Actions)
```

---

## Banco de dados

O arquivo `gastos.db` é gerado automaticamente dentro da pasta `database/`. O esquema possui duas tabelas:

- **categorias** — `id` (UUID), `nome` (único), `descricao`
- **despesas** — `id` (UUID), `descricao`, `valor`, `data`, `categoria_id` (FK → categorias)

Para recriar o banco do zero:

```bash
rm -f database/gastos.db && python3 app.py
```
