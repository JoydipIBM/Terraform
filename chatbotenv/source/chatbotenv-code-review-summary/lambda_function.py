import boto3
import json
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print("api_event",event)
    event = json.loads(event['body'])
    print(event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['table_doc_status'])
    if(len(event['record_Id']) == 0 or event['record_Id'] is None):
        record_Id = ""
    else:
        record_Id = event['record_Id']
    print("record_Id",record_Id)

    if record_Id:
        # Query the table for the specific record_Id
        result = table.query(
            KeyConditionExpression=Key('record_Id').eq(record_Id)
        )
        items = result['Items']
    else:
        # Scan the table for all items
        result = table.scan()
        items = result['Items']

    # Return the appropriate response based on the presence of job_id
    if record_Id and items:
        response_body = json.dumps(items[0], cls=DecimalEncoder)
    else:
        response_body = json.dumps(items, cls=DecimalEncoder)

    return {
        'statusCode': 200,
        'body': response_body,
        'headers': {
            'Access-Control-Allow-Headers': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }
