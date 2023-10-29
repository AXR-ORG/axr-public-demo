# generate a function that creates dynamodb record

import boto3
import json
import os

TEST_TABLE_NAME = os.environ['TEST_TABLE_NAME']

DYNAMODB_RESOURCE = boto3.resource('dynamodb')

TEST_DDB_TABLE = DYNAMODB_RESOURCE.Table(TEST_TABLE_NAME)

def lambda_handler(event, context):
    myTableId = event.get('myTableId')

    tableRecord = getTableRecord(myTableId)

    if not response:
        #create a new record
        createTableRecord(myTableId)

    else:
        #update the existing record
        updateTableRecord(myTableId)


def getTableRecord(myTableId):
    response = TEST_DDB_TABLE.get_item(Key={'myTableId': myTableId}).get('Item')
    return response

def createTableRecord(myTableId):
    TEST_DDB_TABLE.put_item(Item={'myTableId': myTableId, 'myTableValue': 'myTableValue'})

def updateTableRecord(myTableId):
    TEST_DDB_TABLE.update_item(
        Key={'myTableId': myTableId},
        UpdateExpression='SET myTableValue = :myTableValue',
        ExpressionAttributeValues={':myTableValue': 'myTableValue'}
    )