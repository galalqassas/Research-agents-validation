from typing import Optional, Dict, Any, Type, List, Union
import json
import re
from pydantic import BaseModel, ValidationError
from schemas import (
    TitleSummarySchema,
    ActivitySchema,
    RestaurantSchema,
    DishSchema,
    AccommodationSchema,
    TransportSchema
)


def get_schema_for_type(query_type: str) -> Optional[Type[BaseModel]]:
    schema_map = {
        "Activities": ActivitySchema,
        "Restaurants": RestaurantSchema,
        "Dishes": DishSchema,
        "Accomodation": AccommodationSchema,
        "Transport": TransportSchema,
    }
    return schema_map.get(query_type)


def get_all_schema_types() -> List[str]:
    """Get all available schema types."""
    return ["Activities", "Restaurants", "Dishes", "Accomodation", "Transport"]


def validate_json_against_schema(data: Dict[str, Any], schema_type: str) -> tuple[bool, Optional[str]]:
    """Validate JSON data against a specific schema type."""
    try:
        schema_model = get_schema_for_type(schema_type)
        if not schema_model:
            return False, f"Unknown schema type: {schema_type}"
        
        schema_model(**data)
        return True, None
    except ValidationError as e:
        return False, str(e)


def clean_json_string(json_str: str) -> str:
    """Clean and normalize JSON string."""
    # remove whitespace
    cleaned = re.sub(r'\s+', ' ', json_str.strip())
    # remove common formatting issues
    cleaned = re.sub(r',\s*}', '}', cleaned)  # remove trailing commas
    cleaned = re.sub(r',\s*]', ']', cleaned)  # remove trailing commas in arrays
    return cleaned


def extract_multiple_json_objects(text: str) -> List[Dict[str, Any]]:
    """Extract multiple JSON objects from text."""
    json_objects = []
    
    # Find all JSON code blocks
    json_blocks = re.findall(r"```json\s*([\s\S]*?)\s*```", text, re.DOTALL)
    
    for block in json_blocks:
        try:
            cleaned = clean_json_string(block)
            data = json.loads(cleaned)
            json_objects.append(data)
        except json.JSONDecodeError:
            continue
    
    # If no code blocks found, try to find raw JSON objects
    if not json_objects:
        brace_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(brace_pattern, text)
        
        for match in matches:
            try:
                data = json.loads(match)
                json_objects.append(data)
            except json.JSONDecodeError:
                continue
    
    return json_objects


def batch_validate_data(data_list: List[Dict[str, Any]], schema_type: str) -> Dict[str, Any]:
    """Validate multiple data objects and return results summary."""
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

# try
def merge_schema_data(data_list: List[Dict[str, Any]], key_field: str = "Country") -> Dict[str, List[Dict[str, Any]]]:
    """Group schema data by a specific field."""
    grouped = {}
    for data in data_list:
        key = data.get(key_field, "unknown")
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(data)
    return grouped


def extract_and_validate_json_from_text(llm_response_text: str, query_type: str) -> List[Dict[str, Any]]:
    """Extract and validate JSON from text using the specified schema type."""
    SchemaModel = get_schema_for_type(query_type)
    if not SchemaModel:
        return []

    # Try to extract from code blocks first
    json_objects = extract_multiple_json_objects(llm_response_text)
    
    # If no code blocks found, try direct JSON parsing
    if not json_objects:
        stripped_text = llm_response_text.strip()
        if stripped_text.startswith("{") and stripped_text.endswith("}"):
            try:
                json_objects = [json.loads(stripped_text)]
            except json.JSONDecodeError:
                return []
    
    # Validate all found objects
    validated_jsons = []
    for data in json_objects:
        try:
            validated_data = SchemaModel(**data)
            validated_jsons.append(validated_data.model_dump())
        except ValidationError:
            continue
    
    return validated_jsons


def filter_data_by_field(data_list: List[Dict[str, Any]], field: str, value: Any) -> List[Dict[str, Any]]:
    """Filter data by a specific field value."""
    return [item for item in data_list if item.get(field) == value]


def deduplicate_data(data_list: List[Dict[str, Any]], unique_field: str = "name") -> List[Dict[str, Any]]:
    """Remove duplicates based on a specific field."""
    seen = set()
    unique_data = []
    for item in data_list:
        key = item.get(unique_field)
        if key not in seen:
            seen.add(key)
            unique_data.append(item)
    return unique_data


def sort_data_by_field(data_list: List[Dict[str, Any]], field: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """Sort data by a specific field."""
    return sorted(data_list, key=lambda x: x.get(field, ""), reverse=reverse)


def get_schema_fields(schema_type: str) -> List[str]:
    """Get all field names for a specific schema type."""
    schema_model = get_schema_for_type(schema_type)
    if not schema_model:
        return []
    return list(schema_model.model_fields.keys())


def safe_json_parse(text: str) -> Optional[Dict[str, Any]]:
    """Safely parse JSON with error handling."""
    try:
        return json.loads(clean_json_string(text))
    except json.JSONDecodeError:
        return None


def validate_required_fields(data: Dict[str, Any], schema_type: str) -> tuple[bool, List[str]]:
    """Check if all required fields are present in the data."""
    schema_model = get_schema_for_type(schema_type)
    if not schema_model:
        return False, ["Invalid schema type"]
    
    missing_fields = []
    for field_name, field_info in schema_model.model_fields.items():
        if field_info.is_required() and field_name not in data:
            missing_fields.append(field_name)
    
    return len(missing_fields) == 0, missing_fields