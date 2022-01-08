import json
import logging
import todoList

#PGS: Handler for the Type: AWS::Serverless::Function defined in SAM template with:
#Path: /todos
#Method: post
Receives event and context as parameters
def create(event, context):
    #PGS: it receives the request for the creation of a new record as "event" and makes a first validation. 
    #PGS: If the body does not contain 'text', the validation fails
    data = json.loads(event['body'])
    if 'text' not in data:
        #PGS: Append a message in the log and raise and exception
        logging.error("Validation failed")
        raise Exception("Couldn't create the todo item.")
    #PGS: call put_item function, which writes the todo record to the database
    item = todoList.put_item(data['text'])
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }
    return response
