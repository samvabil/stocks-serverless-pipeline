import json
from decimal import Decimal

from backend.services.db import get_recent_winners


def convert_decimals(item: dict) -> dict:
    """
    Converts DynamoDB Decimal values into JSON-safe Python floats
    Removes pk from response
    """
    converted = {}

    for key, value in item.items():
        if key == "pk":
            continue
        converted[key] = float(value) if isinstance(value, Decimal) else value

    return converted


def handler(event, context):
    try:
        winners = get_recent_winners(limit=7)
        response_data = [convert_decimals(item) for item in winners]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": response_data
            })
        }

    except Exception as error:
        print(f"Retrieval failed: {error}")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Retrieval failed",
                "error": str(error)
            })
        }