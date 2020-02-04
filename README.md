# Dataworks
Utilities for working with data in Python.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](http://mypy-lang.org/)
[![Travis build status](https://api.travis-ci.org/bogeholm/dataworks.svg?branch=master)](https://travis-ci.org/bogeholm/dataworks)
[![codecov](https://codecov.io/gh/bogeholm/dataworks/branch/master/graph/badge.svg)](https://codecov.io/gh/bogeholm/dataworks)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[![LGTM alerts](https://img.shields.io/lgtm/alerts/g/bogeholm/dataworks.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bogeholm/dataworks/alerts/)
[![LGTM Quality](https://img.shields.io/lgtm/grade/python/github/bogeholm/dataworks.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bogeholm/dataworks/context:python)
[![Codacy](https://api.codacy.com/project/badge/Grade/44e0328191574bf6bcf63b9e307a0024)](https://app.codacy.com/manual/bogeholm/dataworks/dashboard)
[![Codebeat](https://codebeat.co/badges/12172b77-cbda-4c87-b3ae-c9baf5036e73)](https://codebeat.co/projects/github-com-bogeholm-dataworks-master)


## Testing
[Against local copy](https://docs.pytest.org/en/latest/goodpractices.html):
```bash
python -m pytest
```
With coverage:
```bash
python -m pytest --cov=./
```
Without capturing `stdout`:
```bash
python -m pytest --capture=no
```

## Installing
### Locally
[`pip install .`](https://stackoverflow.com/questions/1471994/what-is-setup-py)

### From GitHub
[`pip install --upgrade git+git://github.com/bogeholm/dataworks.git`](https://stackoverflow.com/questions/15268953/how-to-install-python-package-from-github)

## Packaging
Uses [native namespace packages](https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages) - see [sample-namespace-packages](https://github.com/pypa/sample-namespace-packages/tree/master/native)

