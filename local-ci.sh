#! /bin/bash
echo "---------- black ----------"
black --check --include ./**/*.py --verbose
echo "---------- flake8 ---------"
flake8 --verbose
echo "---------- bandit ---------"
bandit -c bandit.yml *.py