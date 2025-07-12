from typing import Optional, Type, List
from pydantic import BaseModel
from schemas import (
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
        "Accommodation": AccommodationSchema,
        "Transport": TransportSchema,
    }
    return schema_map.get(query_type)


def get_all_schema_types() -> List[str]:
    return ["Activities", "Restaurants", "Dishes", "Accommodation", "Transport"]


def get_schema_fields(schema_type: str) -> List[str]:
    schema_model = get_schema_for_type(schema_type)
    if not schema_model:
        return []
    return list(schema_model.model_fields.keys())
