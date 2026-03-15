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