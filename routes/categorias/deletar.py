from flask import jsonify

from schemas.categoria import CategoriaPath
from schemas.comum import ErroResponse, MensagemResponse
from service import categoria_service
from routes.categorias import bp


@bp.delete(
    "/<categoria_id>",
    responses={"200": MensagemResponse, "404": ErroResponse, "409": ErroResponse},
)
def deletar_categoria(path: CategoriaPath):
    """Deletar uma categoria pelo ID"""
    categoria_service.deletar(path.categoria_id)
    return jsonify({"mensagem": f"Categoria {path.categoria_id} deletada com sucesso"}), 200
