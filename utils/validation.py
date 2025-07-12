from typing import Dict, Any, Optional, List
from pydantic import ValidationError
from .schemas import get_schema_for_type


def validate_json_against_schema(data: Dict[str, Any], schema_type: str) -> tuple[bool, Optional[str]]:
    try:
        schema_model = get_schema_for_type(schema_type)
        if not schema_model:
            return False, f"Unknown schema type: {schema_type}"
        
        schema_model(**data)
        return True, None
    except ValidationError as e:
        return False, str(e)


def validate_required_fields(data: Dict[str, Any], schema_type: str) -> tuple[bool, List[str]]:
    schema_model = get_schema_for_type(schema_type)
    if not schema_model:
        return False, ["Invalid schema type"]
    
    missing_fields = []
    for field_name, field_info in schema_model.model_fields.items():
        if field_info.is_required() and field_name not in data:
            missing_fields.append(field_name)
    
    return len(missing_fields) == 0, missing_fields


def batch_validate_data(data_list: List[Dict[str, Any]], schema_type: str) -> Dict[str, Any]:
    valid_data = []
    errors = []
    
    for i, data in enumerate(data_list):
        is_valid, error = validate_json_against_schema(data, schema_type)
        if is_valid:
            valid_data.append(data)
        else:
            errors.append({"index": i, "error": error})
    
    return {
        "valid_count": len(valid_data),
        "total_count": len(data_list),
        "valid_data": valid_data,
        "errors": errors
    }
