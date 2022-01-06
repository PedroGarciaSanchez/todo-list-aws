import json
import logging
import decimalencoder
import todoList


def update(event, context):
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return
    # update the todo in the database
    result = todoList.update_item(
        event['pathParameters']['id'],
        data['text'], data['checked'])
    # create a response
    #PGS: we use this decimalEncoder workaround as there were problems with 2 fields of the response that contains decimals: createdAt and updatedAt
    response = {
        "statusCode": 200,
        "body": json.dumps(result,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
