from contextlib import contextmanager
from boto3.dynamodb.conditions import Key, Attr

@contextmanager
def dynamodb_table_setup(dynamodbResource, tableName, globalSecondaryIndexes=[]):
    # GSI Stadard Format gsi-xxx-yyy
    gsiConfigs = []
    attributeDefinitions = [{'AttributeName': tableName[0].lower() + tableName[1:] + 'Id','AttributeType': 'S'}]

    for gsi in globalSecondaryIndexes:
        gsiAttributes = gsi.split('-')
        gsiSchemas = [{'AttributeName': gsiAttributes[1], 'KeyType': 'HASH'}]
        if gsiAttributes[1] not in [attributeDefinition.get('AttributeName') for attributeDefinition in attributeDefinitions]:
            attributeDefinitions.append({'AttributeName': gsiAttributes[1],'AttributeType': 'S'})

        if len(gsiAttributes) == 3:
            gsiSchemas.append({'AttributeName': gsiAttributes[2], 'KeyType': 'RANGE'})
            if gsiAttributes[2] not in [attributeDefinition.get('AttributeName') for attributeDefinition in attributeDefinitions]:
                attributeDefinitions.append({'AttributeName': gsiAttributes[2],'AttributeType': 'S'})

        gsiConfigs.append({
            'IndexName': gsi,
            'KeySchema': gsiSchemas,
            'Projection': {'ProjectionType': 'ALL'}
        })

    if gsiConfigs:
        dynamodbResource.create_table(
            TableName=tableName,
            KeySchema=[{'AttributeName': tableName[0].lower() + tableName[1:] + 'Id','KeyType': 'HASH'}],
            AttributeDefinitions=attributeDefinitions,
            BillingMode='PAY_PER_REQUEST',
            GlobalSecondaryIndexes=gsiConfigs
        )
    else:
        dynamodbResource.create_table(
            TableName=tableName,
            KeySchema=[{'AttributeName': tableName[0].lower() + tableName[1:] + 'Id','KeyType': 'HASH'}],
            AttributeDefinitions=attributeDefinitions,
            BillingMode='PAY_PER_REQUEST'
        )
    yield

def DynamoDB_MockTable(dynamodbResource, tableName, globalSecondaryIndexes=[], initialData=[]):
    with dynamodb_table_setup(dynamodbResource, tableName, globalSecondaryIndexes):
        table = dynamodbResource.Table(tableName)
        for item in initialData:
            table.put_item(Item=item)
        return dynamodbResource.Table(tableName)

def dynamodb_get_item(dynamodbResource, tableName, partitionKeyValue):
    table = dynamodbResource.Table(tableName)
    item = table.get_item(Key={tableName[0].lower() + tableName[1:] + 'Id': partitionKeyValue}).get('Item')
    return item
    
def dynamodb_query(dynamodbResource, tableName, tableGsi, partitionKeyValue1, partitionKeyValue2=None):
    table = dynamodbResource.Table(tableName)
    key1 = partitionKeyValue1.get('key')
    value1 = partitionKeyValue1.get('value')
    if partitionKeyValue2:
        key2 = partitionKeyValue2.get('key')
        value2 = partitionKeyValue2.get('value')
        item = table.query(
            IndexName=tableGsi,
            KeyConditionExpression=Key(key1).eq(value1) & Key(key2).eq(value2)
        )
    else:
        item = table.query(
            IndexName=tableGsi,
            KeyConditionExpression=Key(key1).eq(value1)
        )
        
    return item
        