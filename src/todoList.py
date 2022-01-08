import os
import boto3
import time
import uuid
import json
import functools
from botocore.exceptions import ClientError


# PGS: Boto3 facilita la integración de su aplicación, biblioteca
# PGS:  o script de Pythoncon los servicios de AWS,
# PGS: incluidos Amazon S3, Amazon EC2, Amazon DynamoDB y ..

# PGS: functions to operate with the DB.

# PGS: invoked from the functions of this file

def get_table(dynamodb=None):
    if not dynamodb:
        URL = os.environ['ENDPOINT_OVERRIDE']
        # URL = os.environ['DYNAMODB_TABLE']
        # PGS: https://stackoverflow.com/questions/49955926
        # /setting-boto3-dynamodb-endpoint-url-globaly
        # PGS: https://docs.aws.amazon.com/es_es/amazondynamodb/latest/
        # developerguide/DynamoDBLocal.DownloadingAndRunning.html
        # PGS:DynamoURLs:https://docs.aws.amazon.com/general/latest/gr/ddb.html
        # URL = "http://localhost:8000"
        if URL:
            print('URL dynamoDB:'+URL)
            # PGS: By redefining boto3.client and boto3.resource to be our
            # new partial,
            # instead of the original versions from the library, we're
            # monkey-patching boto3.
            # PGS: Monkey patching: It's the dynamic replacement of attributes
            # at runtime.
            # PGS: https://stackoverflow.com/questions/5626193/
            # what-is-monkey-patching
            boto3.client = functools.partial(boto3.client, endpoint_url=URL)
            boto3.resource = functools.partial(boto3.resource,
                                               endpoint_url=URL)
        # dynamodb = boto3.resource("dynamodb")
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # fetch todo from the database
    # PGS: Table: todoUnitTestsTable
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    return table


# PGS: invoked from /todo-list-aws/src/get.py and from TestToDo.py
# PGS key
def get_item(key, dynamodb=None):
    table = get_table(dynamodb)
    try:
        result = table.get_item(
            Key={
                'id': key
            }
        )

    # PGS: ClientError is a Boto exception.
    except ClientError as e:
        print(e.response['Error']['Message'])
    # PGS: if there is no boto3 exception in the recovery of the table
    # and item (todo record)
    else:
        print('Result getItem:'+str(result))
        if 'Item' in result:
            return result['Item']


# PGS: invoked from /todo-list-aws/src/list.py and from TestToDo.py
def get_items(dynamodb=None):
    table = get_table(dynamodb)
    # fetch todo from the database
    result = table.scan()
    return result['Items']


# PGS: invoked from /todo-list-aws/src/create.py  and from TestToDo.py (tests)
def put_item(text, dynamodb=None):
    table = get_table(dynamodb)
    timestamp = str(time.time())
    print('Table name:' + table.name)
    item = {
        'id': str(uuid.uuid1()),
        'text': text,
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    try:
        # write the todo to the database
        table.put_item(Item=item)
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(item)
        }

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


# PGS: invoked from /todo-list-aws/src/update.py  and from TestToDo.py
def update_item(key, text, checked, dynamodb=None):
    table = get_table(dynamodb)
    timestamp = int(time.time() * 1000)
    # update the todo in the database
    try:
        # PGS:https://boto3.amazonaws.com/v1/documentation/api/latest/reference
        # /services/dynamodb.html#DynamoDB.Client.update_item
        result = table.update_item(
            Key={
                'id': key
            },
            ExpressionAttributeNames={
              '#todo_text': 'text',
            },
            ExpressionAttributeValues={
              ':text': text,
              ':checked': checked,
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET #todo_text = :text, '
                             'checked = :checked, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return result['Attributes']


# PGS: invoked from /todo-list-aws/src/delete.py  and from TestToDo.py
def delete_item(key, dynamodb=None):
    table = get_table(dynamodb)
    # delete the todo from the database
    try:
        table.delete_item(
            Key={
                'id': key
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return


# PGS: invoked from /todo-list-aws/test/unit/TestToDo.py
def create_todo_table(dynamodb):
    # For unit testing
    tableName = os.environ['DYNAMODB_TABLE']
    print('Creating Table with name:' + tableName)
    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=tableName)
    if (table.table_status != 'ACTIVE'):
        raise AssertionError()

    return table
