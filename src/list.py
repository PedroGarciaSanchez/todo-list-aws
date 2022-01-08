import json
import decimalencoder
import todoList


def list(event, context):
    # fetch all todos from the database
    result = todoList.get_items()
    # create a response
    # PGS: we use this decimalEncoder workaround as there were problems with
    # PGS: 2 fields
    # PGS: of the response that contains decimals: createdAt and updatedAt
    if result:
        response = {
            "statusCode": 200,
            "body": json.dumps(result, cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response