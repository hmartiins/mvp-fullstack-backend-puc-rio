from flask import jsonify

from schemas.categoria import CategoriaResponse
from service import categoria_service
from routes.categorias import bp


@bp.get("", responses={"200": CategoriaResponse})
def listar_categorias():
    """Listar todas as categorias"""
    return jsonify([c.to_dict() for c in categoria_service.listar()]), 200
