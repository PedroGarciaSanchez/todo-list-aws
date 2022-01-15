#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
#PGS: set variable with table name to use it in todoList.py
export DYNAMODB_TABLE=todoUnitTestsTable
export ENDPOINT_OVERRIDE='http://localhost:8000'

# PGS: start dynamo docker if is exited, for coverage test
if [ ! "$(docker ps -q -f name=dynamodb)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=dynamodb)" ]; then
        docker start -i dynamodb &>/dev/null &
        aws dynamodb create-table --table-name local-TodosDynamoDbTable --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8000 --region us-east-1
    fi
fi
#PGS: Execute TestToDo.py
python test/unit/TestToDo.py
pip show coverage
#PGS: Run a Python program and collect execution data. We must get over 80%
coverage run --include=src/todoList.py test/unit/TestToDo.py
#PGS: Report coverage results. 
coverage report -m
#PGS: Produce an XML report with coverage results.
coverage xml

