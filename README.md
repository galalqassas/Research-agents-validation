# RAVal - Travel Data Validation

A Python project for validating and processing travel-related data using Pydantic schemas.

## Features

- **Pydantic Schemas**: Structured validation for travel data including activities, restaurants, dishes, accommodations, and transport
- **JSON Processing**: Extract and validate JSON data from text responses
- **Type Safety**: Proper type hints and validation using Pydantic

## Usage

```python
from schemas import ActivitySchema, RestaurantSchema
from utils import extract_and_validate_json_from_text

# Validate travel data
validated_data = extract_and_validate_json_from_text(response_text, "Activities")
```

## Schema Types

- **Activities**: Travel activities with budget, duration, and traveler type
- **Restaurants**: Restaurant information with cuisine type and pricing
- **Dishes**: Individual dish details with pricing
- **Accommodations**: Lodging options with nightly rates
- **Transport**: Transportation modes with routes and pricing
- **Title/Summary**: Basic title and summary information
