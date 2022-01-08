#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
#PGS: set variable with table name to use it in todoList.py
export DYNAMODB_TABLE=todoUnitTestsTable
#PGS: Execute TestToDo.py
python test/unit/TestToDo.py
pip show coverage
#PGS: Run a Python program and collect execution data. We must get over 80%
coverage run --include=src/todoList.py test/unit/TestToDo.py
#PGS: Report coverage results.
coverage report -m
#PGS: Produce an XML report with coverage results.
coverage xml