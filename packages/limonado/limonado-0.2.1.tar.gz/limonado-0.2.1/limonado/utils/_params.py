# -*- coding: utf-8 -*-

__all__ = ["extract_params"]

_ITEM_SEPARATORS = {None: None, " ": b" ", ",": b",", "|": b"|"}

_CONVERTERS = {
    "boolean": lambda v: v == b"true" if v in (b"true", b"false") else v,
    "integer": int,
    "null": lambda v: None if v == b"null" else v,
    "number": float,
    "string": lambda v: v.decode("utf-8")
}


def extract_params(arguments, schema):
    properties = schema.get("properties", {})
    additional_properties = schema.get("additionalProperties")
    if isinstance(additional_properties, dict):
        default_subschema = additional_properties
    else:
        default_subschema = None

    params = {}
    for name, values in arguments.items():
        subschema = properties.get(name, default_subschema)
        if subschema is None:
            params[name] = values
        else:
            params[name] = _process_values(values, subschema)

    return params


def _process_values(values, schema):
    if _guess_type(schema) == "array":
        return _convert_array(values, schema)
    elif len(values) == 1:
        return _convert(values[0], schema)

    return values


def _convert_array(values, schema):
    try:
        separator = _ITEM_SEPARATORS[schema.get("itemSeparator")]
    except KeyError:
        raise ValueError("invalid item separator: {}".format(separator))

    if separator is None:
        items = values
    elif values[-1]:
        items = values[-1].split(separator)
    else:
        items = []

    def _get_subschema_for_index(index):
        items = schema["items"]
        if isinstance(items, dict):
            return items

        try:
            return items[index]
        except IndexError:
            additional_items = schema["additionalItems"]
            if isinstance(additional_items, dict):
                return additional_items

            return {"type": "string"}

    return [
        _convert(item, _get_subschema_for_index(i))
        for i, item in enumerate(items)
    ]


def _convert(value, schema):
    type_name = _guess_type(schema)
    if type_name == "object":
        raise ValueError("schema must not contain subordinate objects")

    try:
        return _CONVERTERS[type_name](value)
    except (ValueError, TypeError):
        return value


def _guess_type(schema):
    try:
        return schema["type"]
    except KeyError:
        if "properties" in schema:
            return "object"
        elif "items" in schema:
            return "array"

        return "string"
