#!/bin/bash
#PGS: Activate the venv
source todo-list-aws/bin/activate
#PGS: set -x enables a mode of the shell where all executed commands are printed to the terminal.
set -x
sam validate --region us-east-1
#PGS: sam build: This command iterates through your application's functions, looking for the manifest file (such as requirements.txt or package.json)
#that contains the associated dependencies, automatically creating deployment artifacts.
sam build
