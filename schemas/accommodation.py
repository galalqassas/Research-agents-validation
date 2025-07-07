from pydantic import BaseModel, Field


class AccommodationSchema(BaseModel):
    Country: str = Field(default="unknown")
    City: str = Field(default="unknown")
    AccommodationName: str = Field(default="unknown", alias="Accommodation Name")
    AccommodationDetails: str = Field(default="unknown", alias="Accommodation Details")
    Type: str = Field(default="unknown")
    AvgNightPriceUSD: str = Field(default="unknown", alias="Avg Night Price (USD)")
    
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
