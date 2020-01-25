#! /bin/bash
echo "---------- black ----------"
black --check *.py
echo "---------- flake8 ---------"
flake8 --verbose
echo "---------- bandit ---------"
bandit -c bandit.yml *.py