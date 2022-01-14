#!/bin/bash

source todo-list-aws/bin/activate
set -x
#PGS: We reveive the baseUrl of the stack from the Jenkinsfile, and export it so that todoApiTest.py can use it
export BASE_URL=$1
pytest -s test/integration/todoApiTest.py