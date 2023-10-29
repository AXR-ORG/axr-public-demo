# generate a function that creates dynamodb record

import boto3
import json
import os

TEST_TABLE_NAME = os.environ['TEST_TABLE_NAME']

DYNAMODB_RESOURCE = boto3.resource('dynamodb')

TEST_DDB_TABLE = DYNAMODB_RESOURCE.Table(TEST_TABLE_NAME)

def lambda_handler(event, context):
    testTableId = event.get('testTableId')
    mode = event.get('mode')

    tableRecord = getTableRecord(testTableId)

    if not tableRecord:
        #create a new record
        createTableRecord(testTableId)

    elif mode == "delete":
        #delete the existing record
        deleteTableRecord(testTableId)
    
    else:
        #update the existing record
        updateTableRecord(testTableId)


def getTableRecord(testTableId):
    response = TEST_DDB_TABLE.get_item(Key={'testTableId': testTableId}).get('Item')
    return response

def createTableRecord(testTableId):
    TEST_DDB_TABLE.put_item(Item={'testTableId': testTableId, 'myTableValue': 'myTableValue'})

def updateTableRecord(testTableId):
    TEST_DDB_TABLE.update_item(
        Key={'testTableId': testTableId},
        UpdateExpression='SET myTableValue = :myTableValue',
        ExpressionAttributeValues={':myTableValue': 'myTableValue'}
    )


def deleteTableRecord(testTableId):
    TEST_DDB_TABLE.delete_item(Key={'testTableId': testTableId})
