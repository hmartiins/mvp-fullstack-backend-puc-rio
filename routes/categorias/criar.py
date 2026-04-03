import uuid

from flask import jsonify
from sqlalchemy.exc import IntegrityError

from model.models import db, Categoria
from schemas.categoria import CategoriaInput
from utils import validate_body
from routes.categorias import bp


@bp.route("", methods=["POST"])
@validate_body(CategoriaInput)
def criar_categoria(body: CategoriaInput):
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
      422:
        description: Tipo de campo inválido
        schema:
          $ref: '#/definitions/Erro'
      500:
        description: Erro interno do servidor
        schema:
          $ref: '#/definitions/Erro'
    """
    nome = body.nome.strip()
    descricao = body.descricao.strip() if body.descricao else None

    try:
        categoria = Categoria(id=str(uuid.uuid4()), nome=nome, descricao=descricao)
        db.session.add(categoria)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"erro": f"Já existe uma categoria com o nome '{nome}'"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro interno ao criar categoria", "detalhe": str(e)}), 500

    return jsonify(categoria.to_dict()), 201
