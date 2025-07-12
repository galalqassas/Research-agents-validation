import json
import re
from typing import Dict, Any, List, Optional
from pydantic import ValidationError
from .schemas import get_schema_for_type


def clean_json_string(json_str: str) -> str:
    cleaned = re.sub(r'\s+', ' ', json_str.strip())
    cleaned = re.sub(r',\s*}', '}', cleaned)
    cleaned = re.sub(r',\s*]', ']', cleaned)
    return cleaned


def extract_multiple_json_objects(text: str) -> List[Dict[str, Any]]:
    json_objects = []
    
    json_blocks = re.findall(r"```json\s*([\s\S]*?)\s*```", text, re.DOTALL)
    for block in json_blocks:
        try:
            cleaned = clean_json_string(block)
            data = json.loads(cleaned)
            json_objects.append(data)
        except json.JSONDecodeError:
            continue
    
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


def extract_and_validate_json_from_text(llm_response_text: str, query_type: str) -> List[Dict[str, Any]]:
    SchemaModel = get_schema_for_type(query_type)
    if not SchemaModel:
        return []

    json_objects = extract_multiple_json_objects(llm_response_text)
    
    if not json_objects:
        stripped_text = llm_response_text.strip()
        if stripped_text.startswith("{") and stripped_text.endswith("}"):
            try:
                json_objects = [json.loads(stripped_text)]
            except json.JSONDecodeError:
                return []
    
    validated_jsons = []
    for data in json_objects:
        try:
            validated_data = SchemaModel(**data)
            validated_jsons.append(validated_data.model_dump())
        except ValidationError:
            continue
    
    return validated_jsons


def safe_json_parse(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(clean_json_string(text))
    except json.JSONDecodeError:
        return None
