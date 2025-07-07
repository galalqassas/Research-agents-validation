from pydantic import BaseModel, Field


class ActivitySchema(BaseModel):
    Country: str = Field(default="unknown")
    City: str = Field(default="unknown")
    Activity: str = Field(default="unknown")
    Description: str = Field(default="unknown")
    TypeOfTraveler: str = Field(default="unknown", alias="Type of Traveler")
    Duration: str = Field(default="unknown")
    BudgetUSD: str = Field(default="unknown", alias="Budget (USD)")
    BudgetDetails: str = Field(default="unknown", alias="Budget details")
    Tips: str = Field(default="unknown")
    
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
