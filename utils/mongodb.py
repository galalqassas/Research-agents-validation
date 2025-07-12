from typing import Dict, Any, List
from datetime import datetime
from pymongo import MongoClient
from .validation import batch_validate_data
from .json_utils import extract_and_validate_json_from_text
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_CONNECTION_STRING = f"mongodb+srv://galalqassas:{MONGODB_PASSWORD}@raval.cqt4swq.mongodb.net/?retryWrites=true&w=majority&appName=RAVal"
DATABASE_NAME = "raval"


def get_mongodb_client():
    client = MongoClient(MONGODB_CONNECTION_STRING)
    client.admin.command('ping')
    return client


def get_collection_name(schema_type: str) -> str:
    collection_map = {
        "Activities": "activities",
        "Restaurants": "restaurants", 
        "Dishes": "dishes",
        "Accommodation": "accommodations",
        "Transport": "transport"
    }
    return collection_map.get(schema_type, "unknown")


def insert_validated_data(data_list: List[Dict[str, Any]], schema_type: str) -> Dict[str, Any]:
    if not data_list:
        return {"success": False, "message": "No data to insert", "inserted_count": 0}
    
    client = get_mongodb_client()
    db = client[DATABASE_NAME]
    collection_name = get_collection_name(schema_type)
    collection = db[collection_name]
    
    timestamp = datetime.utcnow()
    for data in data_list:
        data["_inserted_at"] = timestamp
    
    result = collection.insert_many(data_list)
    client.close()
    
    return {
        "success": True,
        "message": f"Inserted {len(result.inserted_ids)} documents",
        "inserted_count": len(result.inserted_ids)
    }


def validate_and_insert_data(llm_response_text: str, schema_type: str) -> Dict[str, Any]:
    validated_data = extract_and_validate_json_from_text(llm_response_text, schema_type)
    
    if not validated_data:
        return {"success": False, "message": "No valid data found", "inserted_count": 0}
    
    return insert_validated_data(validated_data, schema_type)


def batch_validate_and_insert(data_list: List[Dict[str, Any]], schema_type: str) -> Dict[str, Any]:
    validation_result = batch_validate_data(data_list, schema_type)
    
    if validation_result["valid_count"] == 0:
        return {"success": False, "message": "No valid data to insert", "inserted_count": 0}
    
    insert_result = insert_validated_data(validation_result["valid_data"], schema_type)
    
    return {
        **insert_result,
        "validation_summary": {
            "total_count": validation_result["total_count"],
            "valid_count": validation_result["valid_count"],
            "errors": validation_result["errors"]
        }
    }
