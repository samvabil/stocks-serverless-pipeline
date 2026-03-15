# Ingestion Lambda
# Call stock API for each ticker in watchlist, calculate percent change, determine biggest absolute mover, save to DynamoDB

import json

def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "ingest placeholder works",
            "event": event
        })
    }