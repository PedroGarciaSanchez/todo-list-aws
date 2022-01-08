import json
import decimalencoder
import todoList


def get(event, context):
    # create a response
    # PGS: calls get_item function with the id value inside the path parameters
    # PGS: we use this decimalEncoder workaround as there were 
    # PGS: problems with 2 fields of the response
    # PGS: that contains decimals: createdAt and updatedAt
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
