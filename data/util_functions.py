def clean_json_schema(schema: dict) -> dict:
    if isinstance(schema, dict):
        cleaned = {}
        for k, v in schema.items():
            if k in ("$defs", "$ref", "$schema", "title", "description"):
                continue
            if k == "type":
                k = "bsonType"
                if v == "integer":
                    v = "int"
                elif v == "number":
                    v = "double"
                elif v == "boolean":
                    v = "bool"
                elif v == "object":
                    v = "object"
                elif v == "array":
                    v = "array"
                elif v == "string":
                    v = "string"
            cleaned[k] = clean_json_schema(v)
        return cleaned
    elif isinstance(schema, list):
        return [clean_json_schema(item) for item in schema]
    else:
        return schema
