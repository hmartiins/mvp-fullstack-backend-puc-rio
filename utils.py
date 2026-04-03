from datetime import datetime


def parse_date(value: str):
    """Valida e retorna a data no formato YYYY-MM-DD ou lança ValueError."""
    return datetime.strptime(value, "%Y-%m-%d").date()


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


def format_pydantic_errors(errors: list) -> list:
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
