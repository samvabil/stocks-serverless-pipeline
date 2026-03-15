import os
import boto3
from decimal import Decimal

TABLE_NAME = os.environ["MOVERS_TABLE"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def save_winner(item: dict) -> None:
    """Writes stock with largest absolute movement to DynamoDB."""
    dynamo_item = {
        "date": item["date"],
        "ticker": item["ticker"],
        "percentChange": Decimal(str(item["percentChange"])),
        "closingPrice": Decimal(str(item["closingPrice"]))
    }

    table.put_item(Item=dynamo_item)

def get_recent_winners(limit: int = 7) -> list[dict]:
    """
    Gets all items from DynamoDB, sorts by date descending,
    and returns the most recent `limit` items.
    """
    response = table.scan()
    items = response.get("Items", [])

    sorted_items = sorted(items, key=lambda item: item["date"], reverse=True)
    return sorted_items[:limit]