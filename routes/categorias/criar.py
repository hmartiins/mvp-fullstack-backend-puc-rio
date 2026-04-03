import uuid

from flask import jsonify
from sqlalchemy.exc import IntegrityError

from model.models import db, Categoria
from schemas.categoria import CategoriaInput, CategoriaResponse
from schemas.comum import ErroResponse, ErrosResponse
from routes.categorias import bp


@bp.post(
    "",
    responses={"201": CategoriaResponse, "400": ErroResponse, "409": ErroResponse, "422": ErrosResponse},
)
def criar_categoria(body: CategoriaInput):
    """Cadastrar nova categoria"""
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
