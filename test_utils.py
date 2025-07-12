from utils import *
from schemas import ActivitySchema


def test_schema_operations():
    assert get_schema_for_type("Activities") == ActivitySchema
    assert get_schema_for_type("InvalidType") is None
    types = get_all_schema_types()
    assert "Activities" in types and "Restaurants" in types and len(types) == 5


def test_validation():
    data = {"Country": "Japan", "City": "Tokyo", "Activity": "Sushi"}
    is_valid, error = validate_json_against_schema(data, "Activities")
    assert is_valid and error is None
    
    is_valid, error = validate_json_against_schema({}, "InvalidType")
    assert not is_valid and "Unknown schema type" in error


def test_json_processing():
    assert clean_json_string('  { "key": "value",  }  ') == '{ "key": "value"}'
    
    text = '```json\n{"Country": "Japan"}\n```\n```json\n{"Country": "France"}\n```'
    objects = extract_multiple_json_objects(text)
    assert len(objects) == 2 and objects[0]["Country"] == "Japan"
    
    assert safe_json_parse('{"key": "value"}') == {"key": "value"}
    assert safe_json_parse('invalid') is None


def test_batch_operations():
    data = [{"Country": "Japan"}, {"Country": "France"}]
    result = batch_validate_data(data, "Activities")
    assert result["valid_count"] == 2 and result["total_count"] == 2


def test_data_operations():
    data = [{"Country": "Japan", "Activity": "Sushi"}, {"Country": "France", "Activity": "Museum"}]
    grouped = merge_schema_data(data, "Country")
    assert len(grouped["Japan"]) == 1 and len(grouped["France"]) == 1
    
    filtered = filter_data_by_field(data, "Country", "Japan")
    assert len(filtered) == 1
    
    fields = get_schema_fields("Activities")
    assert "Country" in fields and "Activity" in fields


def test_text_extraction():
    text = '```json\n{"Country": "Japan", "Activity": "Sushi"}\n```'
    result = extract_and_validate_json_from_text(text, "Activities")
    assert len(result) == 1 and result[0]["Country"] == "Japan"
    
    result = extract_and_validate_json_from_text(text, "InvalidType")
    assert len(result) == 0


def test_mongodb_functions():
    # Test collection name mapping
    assert get_collection_name("Activities") == "activities"
    assert get_collection_name("Restaurants") == "restaurants"
    assert get_collection_name("InvalidType") == "unknown"
    
    # Test with mock data (without actual MongoDB connection)
    data = [{"Country": "Japan", "Activity": "Test"}]
    # Note: Actual MongoDB tests would require a test database


def test_edge_cases():
    assert batch_validate_data([], "Activities")["valid_count"] == 0
    assert merge_schema_data([]) == {}
    assert filter_data_by_field([], "Country", "Japan") == []


if __name__ == "__main__":
    tests = [test_schema_operations, test_validation, test_json_processing, 
             test_batch_operations, test_data_operations, test_text_extraction, 
             test_mongodb_functions, test_edge_cases]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"FAILED {test.__name__}: {e}")
            exit(1)
    
    print("all tests passed")
