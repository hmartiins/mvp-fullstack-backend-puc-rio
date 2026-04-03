from flask_openapi3 import APIBlueprint, Tag

bp = APIBlueprint("despesas", __name__, url_prefix="/despesas", abp_tags=[Tag(name="Despesas")])

from . import criar, listar, buscar, deletar, resumo, periodo  # noqa: E402, F401
