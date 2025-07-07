from pydantic import BaseModel, Field


class RestaurantSchema(BaseModel):
    Country: str = Field(default="unknown")
    City: str = Field(default="unknown")
    RestaurantName: str = Field(default="unknown", alias="Restaurant Name")
    TypeOfCuisine: str = Field(default="unknown", alias="Type of Cuisine")
    MealsServed: str = Field(default="unknown", alias="Meals Served")
    RecommendedDish: str = Field(default="unknown", alias="Recommended Dish")
    MealDescription: str = Field(default="unknown", alias="Meal Description")
    AvgPricePerPersonUSD: str = Field(default="unknown", alias="Avg Price per Person (USD)")
    BudgetRange: str = Field(default="unknown", alias="Budget Range")
    Suitability: str = Field(default="unknown")
    
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
