from utils import *


def main():
    # Sample LLM response with multiple JSON objects
    llm_response = '''
    ```json
    {"Country": "Japan", "City": "Tokyo", "Activity": "Sushi Making Class", "Description": "Learn traditional sushi making", "TypeOfTraveler": "Foodie", "Duration": "3 hours", "BudgetUSD": "80-120"}
    ```
    ```json
    {"Country": "France", "City": "Paris", "Activity": "Louvre Tour", "Description": "Guided museum tour", "TypeOfTraveler": "Culture", "Duration": "4 hours", "BudgetUSD": "50-70"}
    ```
    ```json
    {"Country": "Thailand", "City": "Bangkok", "Activity": "Temple Tour", "Description": "Visit ancient temples", "TypeOfTraveler": "Culture", "Duration": "2 hours", "BudgetUSD": "20-30"}
    ```
    '''
    
    # Extract and validate activities
    activities = extract_and_validate_json_from_text(llm_response, "Activities")
    print(f"Extracted {len(activities)} valid activities")
    
    # Insert activities into MongoDB
    if activities:
        insert_result = insert_validated_data(activities, "Activities")
        print(f"MongoDB Insert Result: {insert_result}")
    
    # Sample restaurant and accommodation data
    restaurant = {
        "Country": "Italy", "City": "Rome", "RestaurantName": "Trattoria Roma",
        "TypeOfCuisine": "Italian", "MealsServed": "Lunch, Dinner",
        "RecommendedDish": "Carbonara", "MealDescription": "Authentic pasta",
        "AvgPricePerPersonUSD": "25-35"
    }
    
    accommodation = {
        "Country": "Spain", "City": "Barcelona", "AccommodationName": "Hotel Barcelona",
        "TypeOfAccommodation": "Hotel", "StarRating": "4", "PricePerNightUSD": "120-180",
        "Description": "Modern hotel in city center"
    }
    
    # Validate and insert restaurant
    restaurant_valid, _ = validate_json_against_schema(restaurant, "Restaurants")
    if restaurant_valid:
        restaurant_insert = insert_validated_data([restaurant], "Restaurants")
        print(f"Restaurant Insert: {restaurant_insert}")
    
    # Validate and insert accommodation  
    accommodation_valid, _ = validate_json_against_schema(accommodation, "Accommodation")
    if accommodation_valid:
        accommodation_insert = insert_validated_data([accommodation], "Accommodation")
        print(f"Accommodation Insert: {accommodation_insert}")
    
    # Demonstrate batch validation and insertion
    mixed_activities = [
        {"Country": "Spain", "City": "Madrid", "Activity": "Prado Museum", "Description": "Art museum visit", "Duration": "2 hours", "BudgetUSD": "15"},
        {"Country": "Germany", "City": "Berlin", "Activity": "Brandenburg Gate", "Description": "Historic landmark", "Duration": "1 hour", "BudgetUSD": "0"}
    ]
    
    batch_result = batch_validate_and_insert(mixed_activities, "Activities")
    print(f"Batch Insert Result: {batch_result}")
    
    # Data operations
    all_activities = activities + batch_result.get('validation_summary', {}).get('valid_count', 0) * [{}]
    grouped = merge_schema_data(activities, "Country")
    culture_activities = filter_data_by_field(activities, "TypeOfTraveler", "Culture")
    sorted_activities = sort_data_by_field(activities, "Country")
    deduplicated = deduplicate_data(activities, "Activity")
    
    # Schema utilities
    activity_fields = get_schema_fields("Activities")
    all_types = get_all_schema_types()
    
    return {
        "extracted_activities": len(activities),
        "restaurant_valid": restaurant_valid,
        "accommodation_valid": accommodation_valid,
        "batch_valid": batch_result.get('validation_summary', {}).get('valid_count', 0),
        "countries": list(grouped.keys()),
        "culture_activities": len(culture_activities),
        "total_unique": len(deduplicated),
        "schema_types": len(all_types),
        "activity_fields": len(activity_fields)
    }


if __name__ == "__main__":
    result = main()
    print(f"Activities: {result['extracted_activities']}, Valid restaurant: {result['restaurant_valid']}")
    print(f"Countries: {result['countries']}, Culture activities: {result['culture_activities']}")
    print(f"Activity fields: {result['activity_fields']}")