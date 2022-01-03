#!/bin/bash

set -x
#PGS:create and activate venv
python3.7 -m venv todo-list-aws
source todo-list-aws/bin/activate
#PGS: get the latest version of pip
python -m pip install --upgrade pip

#For static testing: static_test.sh

#PGS: Radon is a Python tool which computes various code metrics. Supported metrics are:
#raw metrics: SLOC, comment lines, blank lines, &c.
#Cyclomatic Complexity (i.e. McCabe’s Complexity)
#Halstead metrics (all of them)
#the Maintainability Index (a Visual Studio metric)
python -m pip install radon
#PGS: Flake8 is a wrapper around these tools:
#PyFlakes: A simple program which checks Python source files for errors.Pyflakes analyzes programs and detects various errors. 
#It works by parsing the source file, not importing it, so it is safe to use on modules with side effects. It’s also much faster.
#pycodestyle: pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.
#Ned Batchelder’s McCabe script: Ned’s script to check McCabe complexity (cyclomatic comolexity).
#Flake8 runs all the tools by launching the single flake8 command. It displays the warnings in a per-file, merged output.
python -m pip install flake8
#PGS: flake8-polyfill is a package that provides some compatibility helpers for Flake8 plugins that intend to support Flake8 2.x and 3.x simultaneously.
python -m pip install flake8-polyfill
#PGS: Bandit is a tool designed to find common security issues in Python code. To do this Bandit processes each file, builds an AST from it, 
#and runs appropriate plugins against the AST nodes. Once Bandit has finished scanning all the files it generates a report.
python -m pip install bandit

#For integration testing

#The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.
python -m pip install pytest

#For unit testing: unit_test.sh

#PGS: You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services, such as Amazon Elastic Compute Cloud 
#(Amazon EC2) and Amazon Simple Storage Service (Amazon S3).
python -m pip install boto3
#PGS: Moto is a library that allows your tests to easily mock out AWS Services. In this project we use mock_dynamodb2 from moto
python -m pip install moto
#PGS: mock is a library for testing in Python. It allows you to replace parts of your system under test with mock objects and make assertions
#about how they have been used. Mock is now part of the Python standard library, available as unittest.mock in Python 3.3 onwards.
python -m pip install mock==4.0.2
#PGS: Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code
#have been executed, then analyzes the source to identify code that could have been executed but was not.
#Coverage measurement is typically used to gauge the effectiveness of tests. 
python -m pip install coverage==4.5.4


pwd