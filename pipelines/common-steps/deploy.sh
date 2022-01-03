#!/bin/bash

#PGS: set -x enables a mode of the shell where all executed commands are printed to the terminal.
set -x
#PGS: du = disk usage:
#Pipeline Console output:
#+ du -hs 
# CHANGELOG.md README.md coverage.xml localEnvironment.json pipelines pytest.ini samconfig.toml src template.yaml test todo-list-aws
# 4.0K    CHANGELOG.md
# 4.0K    coverage.xml
# 4.0K    localEnvironment.json
# 4.0K    pytest.ini
# 4.0K    samconfig.toml
# 8.0K    README.md
# 8.0K    template.yaml
# 28K     test
# 48K     src
# 60K     pipelines
# 149M    todo-list-aws
du -hs * | sort -h

#PGS: deploy the artifacts through the stack of the AWS CloudFormation service
#Not guided, but called using template.yaml
#Staging: sam deploy template.yaml --config-env staging
#Prod:    sam deploy template.yaml --config-env prod
#template.yaml defines the application's AWS resources: CreateTodoFunction, ListTodosFunction, GetTodoFunction, UpdateTodoFunction,
#DeleteTodoFunction, TodosDynamoDbTable
sam deploy template.yaml --config-env ${ENVIRONMENT} --no-confirm-changeset --force-upload --no-fail-on-empty-changeset --no-progressbar
