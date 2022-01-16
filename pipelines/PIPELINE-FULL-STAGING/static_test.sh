#!/bin/bash

#PGS: activates the virtual environment
source todo-list-aws/bin/activate
#PGS: set -x enables a mode of the shell where all executed commands are printed to the terminal.
set -x

#PGS: Radon tests. cc is the radon command to compute Cyclomatic Complexity.
#src is the folder to test.
#-nc tells radon to print only results with a complexity rank of C or worse.
# We get the output; error if not equal to 0.
RAD_ERRORS=$(radon cc src -nc | wc -l)

if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - CC'
    exit 1
fi
RAD_ERRORS=$(radon mi src -nc | wc -l)
if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - MI'
    exit 1
fi

#PGS: flake 8 execution over python files in src folder
flake8 --ignore=E501,E121 src/*.py
if [[ $? -ne 0 ]]
then
    exit 1
fi
#PGS: bandit execution over python files in src folder
bandit src/*.py
if [[ $? -ne 0 ]]
then
    exit 1
fi
#PGS: An error in any of these tests will make the script fail with exit 1 
