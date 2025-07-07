from pydantic import BaseModel, Field


class DishSchema(BaseModel):
    Country: str = Field(default="unknown")
    City: str = Field(default="unknown")
    DishName: str = Field(default="unknown", alias="Dish Name")
    DishDetails: str = Field(default="unknown", alias="Dish Details")
    Type: str = Field(default="unknown")
    AvgPriceUSD: str = Field(default="unknown", alias="Avg Price (USD)")
    BestFor: str = Field(default="unknown", alias="Best For")
    
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
