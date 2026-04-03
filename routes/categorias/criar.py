import uuid

from flask import request, jsonify

from models import get_db
from routes.categorias import bp


@bp.route("", methods=["POST"])
def criar_categoria():
    """
    Cadastrar nova categoria
    ---
    tags:
      - Categorias
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/CategoriaInput'
    responses:
      201:
        description: Categoria criada com sucesso
        schema:
          $ref: '#/definitions/Categoria'
      400:
        description: Dados inválidos ou campo obrigatório ausente
        schema:
          $ref: '#/definitions/Erro'
      409:
        description: Categoria com esse nome já existe
        schema:
          $ref: '#/definitions/Erro'
      500:
        description: Erro interno do servidor
        schema:
          $ref: '#/definitions/Erro'
    """
    data = request.get_json(silent=True)
    if not data or not data.get("nome", "").strip():
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    nome = data["nome"].strip()
    descricao = data.get("descricao", "").strip() or None

    try:
        conn = get_db()
        cursor = conn.cursor()
        categoria_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO categorias (id, nome, descricao) VALUES (?, ?, ?)",
            (categoria_id, nome, descricao),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        if "UNIQUE" in str(e):
            return jsonify({"erro": f"Já existe uma categoria com o nome '{nome}'"}), 409
        return jsonify({"erro": "Erro interno ao criar categoria", "detalhe": str(e)}), 500

    return jsonify({"id": categoria_id, "nome": nome, "descricao": descricao}), 201
