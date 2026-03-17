import json
from decimal import Decimal

from backend.services.db import get_recent_winners

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}


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


def build_response(status_code: int, payload: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": DEFAULT_HEADERS,
        "body": json.dumps(payload)
    }


def handler(event, context):
    try:
        if (event or {}).get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
            return build_response(200, {"message": "ok"})

        winners = get_recent_winners(limit=7)
        response_data = [convert_decimals(item) for item in winners]

        return build_response(200, {
            "data": response_data
        })

    except Exception as error:
        print(f"Retrieval failed: {error}")

        return build_response(500, {
            "message": "Retrieval failed",
            "error": str(error)
        })
