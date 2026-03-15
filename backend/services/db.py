import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ["MOVERS_TABLE"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
WINNERS_PARTITION_KEY = "WINNER"

def save_winner(item: dict) -> None:
    """Writes stock with largest absolute movement to DynamoDB."""
    dynamo_item = {
        "pk": WINNERS_PARTITION_KEY,
        "date": item["date"],
        "ticker": item["ticker"],
        "percentChange": Decimal(str(item["percentChange"])),
        "closingPrice": Decimal(str(item["closingPrice"]))
    }

    table.put_item(Item=dynamo_item)

def get_recent_winners(limit: int = 7) -> list[dict]:
    """
    Queries the winners partition by date descending and returns
    the most recent `limit` items.
    """
    response = table.query(
        KeyConditionExpression=Key("pk").eq(WINNERS_PARTITION_KEY),
        ScanIndexForward=False,
        Limit=limit
    )
    return response.get("Items", [])
