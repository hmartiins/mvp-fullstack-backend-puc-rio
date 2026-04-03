from flask import Blueprint

bp = Blueprint("despesas", __name__, url_prefix="/despesas")

from . import criar, listar, buscar, deletar, resumo, periodo  # noqa: E402, F401
