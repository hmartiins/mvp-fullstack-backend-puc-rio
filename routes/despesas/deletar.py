from flask import jsonify

from schemas.despesa import DespesaPath
from schemas.comum import ErroResponse, MensagemResponse
from service import despesa_service
from routes.despesas import bp


@bp.delete("/<despesa_id>", responses={"200": MensagemResponse, "404": ErroResponse})
def deletar_despesa(path: DespesaPath):
    """Deletar uma despesa pelo ID"""
    despesa_service.deletar(path.despesa_id)
    return jsonify({"mensagem": f"Despesa {path.despesa_id} deletada com sucesso"}), 200
