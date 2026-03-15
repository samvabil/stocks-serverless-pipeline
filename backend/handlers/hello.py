def handler(event, context):
    return {
        "statusCode": 200,
        "body": '{"message": "hello from lambda"}',
        "headers": {
            "Content-Type": "application/json"
        }
    }