import re
from functools import reduce


EXPRESSION_REGEX = re.compile(r"\{\{([^}]+)\}\}")


def _resolve_path(context: dict, path: str) -> any:
    """Safely gets a value from a nested dict using dot notation."""
    try:
        return reduce(lambda d, key: d[key], path.strip().split("."), context)
    except (KeyError, TypeError):
        return None


def parse_expression(template: str, context: dict) -> str:
    """Parses a string, replacing all {{...}} expressions."""

    def replacer(match):
        path = match.group(1)
        resolved_value = _resolve_path(context, path)

        if resolved_value is None:
            return ""

        return str(resolved_value)

    return EXPRESSION_REGEX.sub(replacer, template)


def resolve_parameters(
    parameters: dict | list | str, context: dict
) -> dict | list | str:
    """Recursively resolves expressions in nested dicts, lists, and strings."""
    if isinstance(parameters, str):
        return parse_expression(parameters, context)
    if isinstance(parameters, dict):
        return {k: resolve_parameters(v, context) for k, v in parameters.items()}
    if isinstance(parameters, list):
        return [resolve_parameters(item, context) for item in parameters]
    return parameters
