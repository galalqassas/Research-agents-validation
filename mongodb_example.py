#!/usr/bin/env python3
"""
MongoDB integration example with RAVal
"""

from utils import validate_and_insert_data, batch_validate_and_insert

def main():
    # Extract and insert from LLM response
    llm_text = '''
    ```json
    {"Country": "Japan", "City": "Tokyo", "Activity": "Sushi Making Class", "Description": "Learn traditional sushi making", "TypeOfTraveler": "Foodie", "Duration": "3 hours", "BudgetUSD": "80-120"}
    ```
    '''
    
    validate_and_insert_data(llm_text, "Activities")
    
    # Batch validate and insert restaurants
    restaurants = [
        {
            "Country": "Italy", 
            "City": "Rome", 
            "RestaurantName": "Trattoria Roma",
            "TypeOfCuisine": "Italian", 
            "MealsServed": "Lunch, Dinner",
            "RecommendedDish": "Carbonara", 
            "MealDescription": "Authentic pasta",
            "AvgPricePerPersonUSD": "25-35"
        },
        {
            "Country": "France", 
            "City": "Paris", 
            "RestaurantName": "Le Petit Bistro",
            "TypeOfCuisine": "French", 
            "MealsServed": "Dinner",
            "RecommendedDish": "Coq au Vin", 
            "MealDescription": "Traditional French chicken",
            "AvgPricePerPersonUSD": "45-60"
        }
    ]
    
    print(batch_validate_and_insert(restaurants, "Restaurants"))
    
    # Insert accommodation data
    accommodations = [
        {
            "Country": "Spain", 
            "City": "Barcelona", 
            "AccommodationName": "Hotel Barcelona",
            "AccommodationDetails": "Modern hotel in city center",
            "Type": "Hotel", 
            "AvgNightPriceUSD": "120-180"
        }
    ]
    
    print(batch_validate_and_insert(accommodations, "Accommodation"))

if __name__ == "__main__":
    main()
