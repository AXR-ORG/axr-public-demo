#generate a function that inserts data to DynamoDB table

import boto3
import json
import decimal
import os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    response = table.put_item(Item=event)
    return response