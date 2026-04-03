from flask import jsonify

from schemas.categoria import CategoriaInput, CategoriaResponse
from schemas.comum import ErroResponse, ErrosResponse
from service import categoria_service
from routes.categorias import bp


@bp.post(
    "",
    responses={"201": CategoriaResponse, "409": ErroResponse, "422": ErrosResponse},
)
def criar_categoria(body: CategoriaInput):
    """Cadastrar nova categoria"""
    nome = body.nome.strip()
    descricao = body.descricao.strip() if body.descricao else None

    categoria = categoria_service.criar(nome, descricao)
    return jsonify(categoria.to_dict()), 201
