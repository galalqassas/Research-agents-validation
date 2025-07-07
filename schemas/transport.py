from pydantic import BaseModel, Field


class TransportSchema(BaseModel):
    Country: str = Field(default="unknown")
    From: str = Field(default="unknown")
    To: str = Field(default="unknown")
    TransportMode: str = Field(default="unknown", alias="Transport Mode")
    Provider: str = Field(default="unknown")
    Schedule: str = Field(default="unknown")
    RouteInfo: str = Field(default="unknown", alias="Route Info")
    DurationInHours: str = Field(default="unknown", alias="Duration in hours")
    PriceRangeInUSD: str = Field(default="unknown", alias="Price Range in USD")
    CostDetailsAndOptions: str = Field(default="unknown", alias="Cost Details and Options")
    AdditionalInfo: str = Field(default="unknown")
    
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
