from datetime import datetime
from functools import wraps

from flask import request, jsonify
from pydantic import ValidationError


def parse_date(value: str):
    """Valida e retorna a data no formato YYYY-MM-DD ou lança ValueError."""
    return datetime.strptime(value, "%Y-%m-%d").date()


def row_to_dict(row) -> dict:
    return dict(row) if row else None


def _json_type_name(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    return type(value).__name__


def _format_pydantic_errors(errors: list) -> list:
    messages = []
    for err in errors:
        field = err["loc"][0] if err["loc"] else "?"
        err_type = err["type"]
        input_val = err.get("input")

        if err_type == "missing":
            messages.append(f"O campo '{field}' é obrigatório")
        elif err_type == "string_type":
            messages.append(
                f"O campo '{field}' deve ser do tipo string, "
                f"mas foi recebido {_json_type_name(input_val)}"
            )
        elif err_type in ("float_type", "int_type", "float_parsing"):
            messages.append(
                f"O campo '{field}' deve ser do tipo number, "
                f"mas foi recebido {_json_type_name(input_val)}"
            )
        elif err_type == "greater_than":
            messages.append(f"O campo '{field}' deve ser maior que 0")
        elif err_type == "string_too_short":
            messages.append(f"O campo '{field}' não pode estar vazio")
        elif err_type == "value_error":
            messages.append(f"O campo '{field}' {err['ctx']['error']}")
        else:
            messages.append(f"O campo '{field}': {err['msg']}")

    return messages


def validate_body(schema_class):
    """
    Decorator que valida o corpo da requisição contra um schema Pydantic.
    Injeta o objeto validado como `body` na função da rota.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"erro": "Corpo da requisição inválido ou ausente"}), 400
            try:
                kwargs["body"] = schema_class.model_validate(data)
            except ValidationError as e:
                return jsonify({"erros": _format_pydantic_errors(e.errors())}), 422
            return f(*args, **kwargs)
        return wrapper
    return decorator
