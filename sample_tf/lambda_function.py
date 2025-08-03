def handler(event, context):
    """
    Simple Lambda function handler
    """
    return {
        'statusCode': 200,
        'body': f'Hello from Lambda! Event: {event}'
    }
