from typing import Dict, Any, List


def merge_schema_data(data_list: List[Dict[str, Any]], key_field: str = "Country") -> Dict[str, List[Dict[str, Any]]]:
    grouped = {}
    for data in data_list:
        key = data.get(key_field, "unknown")
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(data)
    return grouped


def filter_data_by_field(data_list: List[Dict[str, Any]], field: str, value: Any) -> List[Dict[str, Any]]:
    return [item for item in data_list if item.get(field) == value]


def deduplicate_data(data_list: List[Dict[str, Any]], unique_field: str = "name") -> List[Dict[str, Any]]:
    seen = set()
    unique_data = []
    for item in data_list:
        key = item.get(unique_field)
        if key not in seen:
            seen.add(key)
            unique_data.append(item)
    return unique_data


def sort_data_by_field(data_list: List[Dict[str, Any]], field: str, reverse: bool = False) -> List[Dict[str, Any]]:
    return sorted(data_list, key=lambda x: x.get(field, ""), reverse=reverse)
