import todoList


#PGS: handler invoked from /todo-list-aws/template.yaml
def delete(event, context):
    todoList.delete_item(event['pathParameters']['id'])

    # create a response
    response = {
        "statusCode": 200
    }

    return response
