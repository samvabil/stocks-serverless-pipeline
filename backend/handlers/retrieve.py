# Retrieval Lambda
# read last 7 days from Dynamodb, return JSON

# convert Decimal back to float or str before returning JSON

import json

def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "data": [],
            "message": "get_movers placeholder works"
        })
    }