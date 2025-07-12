# RAVal - Research Agents Data Validation

## Usage

### Basic Validation

```python
from schemas import ActivitySchema
from utils import extract_and_validate_json_from_text

validated_data = extract_and_validate_json_from_text(response_text, "Activities")
```

### MongoDB Integration

```python
from utils import validate_and_insert_data, batch_validate_and_insert

# extract, validate and insert from an LLM response
result = validate_and_insert_data(llm_response_text, "Activities")

# batch validate and insert data 
result = batch_validate_and_insert(data_list, "Restaurants") 
```

## Schema Types

- **Activities** → `activities` collection
- **Restaurants** → `restaurants` collection
- **Dishes** → `dishes` collection
- **Accommodations** → `accommodations` collection
- **Transport** → `transport` collection
- **Title/Summary** → `title_summary` collection