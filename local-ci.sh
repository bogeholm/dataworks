#! /bin/bash

echo "---------- tests ----------"
python -m pytest

echo "---------- black ----------"
black --check --verbose .

echo "---------- flake8 ---------"
flake8 --verbose

echo "---------- bandit ---------"
bandit --configfile bandit.yml --recursive .

echo "---------- mypy -----------"
mypy --config-file=mypy.ini dataworks/
