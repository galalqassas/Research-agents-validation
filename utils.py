from typing import Optional, Dict, Any, Type
import json
import re
from pydantic import BaseModel
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


def extract_json_section(result_str: str) -> Optional[Dict[str, Any]]:
    cleaned_str = re.sub(r'(?<=\n)[ ]+', ' ', result_str)
    cleaned_str = re.sub(r'(?<!\n)[ ]{2,}', ' ', cleaned_str)

    json_start = cleaned_str.find('{')
    if json_start == -1:
        print("No JSON object found in the response")
        return None

    brace_count = 0
    json_end = -1
    for i, char in enumerate(cleaned_str[json_start:]):
        if char == '{': 
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                json_end = json_start + i + 1
                break

    json_str = cleaned_str[json_start:json_end]
    data = json.loads(json_str)
    validated_data = TitleSummarySchema(**data)
    return validated_data.model_dump()


def extract_and_validate_json_from_text(llm_response_text: str, query_type: str):
    validated_jsons = []
    SchemaModel = get_schema_for_type(query_type)

    if not SchemaModel:
        print(f"No Pydantic schema found for query type: {query_type}")
        return []

    json_pattern = r"```json\s*([\s\S]*?)\s*```"
    match = re.search(json_pattern, llm_response_text, re.DOTALL)

    json_str_to_parse = None
    if match:
        json_str_to_parse = match.group(1).strip()
    else:
        stripped_text = llm_response_text.strip()
        if stripped_text.startswith("{") and stripped_text.endswith("}"):
            json_str_to_parse = stripped_text

    data = json.loads(json_str_to_parse)
    validated_data = SchemaModel(**data)
    validated_jsons.append(validated_data.model_dump())

    return validated_jsons