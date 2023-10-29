import pytest
import os
import importlib
import boto3
from moto import mock_dynamodb
from datetime import datetime
from botocore.exceptions import ClientError

os.environ['TEST_TABLE_NAME'] = 'TestTable'

FILE_NAME = "lambda.Functions.MyTest"
DDB_MOCK = "mock_services_setup.dynamodb_mock"

sampleData = [
    {
        'testTableId': 'testTableId1',
        'myTableValue': 'myTableValue1'
    },
    {
        'testTableId': 'testTableId2',
        'myTableValue': 'myTableValue2'
    },
    {
        'testTableId': 'testTableId3',
        'myTableValue': 'myTableValue3'
    }

]
# @pytest.fixture(scope="function")
# def events():
#     return None

def test_create_ddb_tables(dynamodb_resource):
    dynamodb_mock = importlib.import_module(DDB_MOCK)
    
    #initialize table
    testTable = dynamodb_mock.DynamoDB_MockTable(dynamodb_resource, "TestTable", [], sampleData)
    

def test_create_record(dynamodb_resource, lambda_context):
    #import lambda function
    lambda_function = importlib.import_module("{}.lambda_function".format(FILE_NAME))
    dynamodb_mock = importlib.import_module(DDB_MOCK)

    #create event
    event = {'testTableId': 'testTableId4'}
    
    #call lambda function
    lambda_function.lambda_handler(event, lambda_context)
    
    #get table record
    response = dynamodb_mock.dynamodb_get_item(dynamodb_resource, "TestTable", 'testTableId4')
    
    assert response.get('testTableId') == 'testTableId4'
    assert response.get('myTableValue') == 'myTableValue'


def test_update_record(dynamodb_resource, lambda_context):
    #import lambda function
    lambda_function = importlib.import_module("{}.lambda_function".format(FILE_NAME))
    dynamodb_mock = importlib.import_module(DDB_MOCK)

    #update record
    event = {'testTableId': 'testTableId1'}
    
    #call lambda function
    lambda_function.lambda_handler(event, lambda_context)
    
    #get table record
    response = dynamodb_mock.dynamodb_get_item(dynamodb_resource, "TestTable", 'testTableId1')
    
    assert response.get('testTableId') == 'testTableId1'
    assert response.get('myTableValue') == 'myTableValue'


def test_get_record(dynamodb_resource, lambda_context, mocker):
    lambda_function = importlib.import_module("{}.lambda_function".format(FILE_NAME))
    
    #get existing record
    record = lambda_function.getTableRecord('testTableId4')
    assert record.get('testTableId') == 'testTableId4'

    #get non-existing record
    record = lambda_function.getTableRecord('testTableId5')
    assert record == None

