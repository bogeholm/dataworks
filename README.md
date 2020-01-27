# Dataworks
Utilities for working with data in Python.

[![Total alerts](https://img.shields.io/lgtm/alerts/g/bogeholm/dataworks.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bogeholm/dataworks/alerts/)
[![Codebeat](https://codebeat.co/badges/12172b77-cbda-4c87-b3ae-c9baf5036e73)](https://codebeat.co/projects/github-com-bogeholm-dataworks-master)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)


## Testing
[Against local copy](https://docs.pytest.org/en/latest/goodpractices.html):
```python
python -m pytest
```
With coverage:
```python
python -m pytest --cov=./
```

## Installing
### Locally
[`pip install .`](https://stackoverflow.com/questions/1471994/what-is-setup-py)

### From GitHub
[`pip install --upgrade git+git://github.com/bogeholm/dataworks.git`](https://stackoverflow.com/questions/15268953/how-to-install-python-package-from-github)

## Packaging
Uses [native namespace packages](https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages) - see [sample-namespace-packages](https://github.com/pypa/sample-namespace-packages/tree/master/native)

