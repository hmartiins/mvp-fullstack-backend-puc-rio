from flask_openapi3 import APIBlueprint, Tag

bp = APIBlueprint("categorias", __name__, url_prefix="/categorias", abp_tags=[Tag(name="Categorias")])

from . import criar, listar, deletar  # noqa: E402, F401
