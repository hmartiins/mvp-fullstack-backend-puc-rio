SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Controle de Gastos Pessoais",
        "description": "API REST para registrar e consultar gastos pessoais organizados por categorias.",
        "version": "1.0.0",
        "contact": {"email": "contato@exemplo.com"},
    },
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "definitions": {
        "Categoria": {
            "type": "object",
            "properties": {
                "id":        {"type": "string", "example": "550e8400-e29b-41d4-a716-446655440000"},
                "nome":      {"type": "string", "example": "Alimentação"},
                "descricao": {"type": "string", "example": "Gastos com refeições"},
            },
        },
        "CategoriaInput": {
            "type": "object",
            "required": ["nome"],
            "properties": {
                "nome":      {"type": "string", "example": "Transporte"},
                "descricao": {"type": "string", "example": "Ônibus, metrô, combustível"},
            },
        },
        "Despesa": {
            "type": "object",
            "properties": {
                "id":             {"type": "string", "example": "550e8400-e29b-41d4-a716-446655440000"},
                "descricao":      {"type": "string", "example": "Almoço no restaurante"},
                "valor":          {"type": "number", "example": 35.50},
                "data":           {"type": "string", "example": "2024-03-15"},
                "categoria_id":   {"type": "string", "example": "550e8400-e29b-41d4-a716-446655440000"},
                "categoria_nome": {"type": "string", "example": "Alimentação"},
            },
        },
        "DespesaInput": {
            "type": "object",
            "required": ["descricao", "valor", "data", "categoria_id"],
            "properties": {
                "descricao":    {"type": "string", "example": "Gasolina"},
                "valor":        {"type": "number", "example": 120.00},
                "data":         {"type": "string", "example": "2024-03-20"},
                "categoria_id": {"type": "string", "example": "550e8400-e29b-41d4-a716-446655440000"},
            },
        },
        "Resumo": {
            "type": "object",
            "properties": {
                "categoria_id":   {"type": "string", "example": "550e8400-e29b-41d4-a716-446655440000"},
                "categoria_nome": {"type": "string", "example": "Alimentação"},
                "total":          {"type": "number", "example": 450.75},
                "quantidade":     {"type": "integer", "example": 12},
            },
        },
        "Erro": {
            "type": "object",
            "properties": {
                "erro": {"type": "string", "example": "Recurso não encontrado"},
            },
        },
    },
}

SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs",
}
