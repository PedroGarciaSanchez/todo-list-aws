import json
import decimalencoder
import todoList


def list(event, context):
    # fetch all todos from the database
    result = todoList.get_items()
    # create a response
    #PGS: we use this decimalEncoder workaround as there were problems with 2 fields of the response that contains decimals: createdAt and updatedAt
    response = {
        "statusCode": 200,
        "body": json.dumps(result, cls=decimalencoder.DecimalEncoder)
    }
    return response
